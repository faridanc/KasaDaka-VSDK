from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from ..models import *
import datetime


def veterinarian_selection_options_resolve_voice_labels(selection_options, language):
    """
    Returns a list of voice labels belonging to the provided list of selection_options.
    """
    selection_options_voice_labels = []
    for selection_option in selection_options:
        selection_options_voice_labels.append(selection_option.get_voice_fragment_url(language))
    return selection_options_voice_labels

def veterinarian_selection_generate_context(selection_element, session, region):
    """
    Returns a dict that can be used to generate the selection VXML template
    selection = this selection element object
    selection_voice_label = the resolved Voice Label URL for this selection element
    selection_options = iterable of selectionOption object belonging to this selection element
    selection_options_voice_labels = list of resolved Voice Label URL's referencing to the selection_options in the same position
    selection_options_redirect_urls = list of resolved redirection URL's referencing to the selection_options in the same position
        """
    "only lists vet in selected region"
    availableVetId = Veterinarian.objects.filter(region_id=region).values_list('id', flat=True)

    if availableVetId:
        selection_options = selection_element.selection_options.filter(options_id__in=availableVetId)
    else:
        selection_options =  selection_element.selection_options.all()
    
    language = session.language

    redirect_url = selection_element.redirect.get_absolute_url(session)
    
    context = {'selection':selection_element,
                'selection_voice_label':selection_element.get_voice_fragment_url(language),
                'selection_options': selection_options,
                'selection_options_voice_labels': veterinarian_selection_options_resolve_voice_labels(selection_options, language),
                'language': language,
                'redirect_url': redirect_url
             }
    return context

def veterinarian_selection(request, element_id, session_id):
    selection_element = get_object_or_404(VeterinarianSelection, pk=element_id)
    session = get_object_or_404(CallSession, pk=session_id)
    session.record_step(selection_element)

    if request.method == "POST" and request.POST['region_id']:
        region_id = request.POST['region_id']
        session.region = region_id
        session.save()

    context = veterinarian_selection_generate_context(selection_element, session, region_id)
      
    return render(request, 'veterinarian_selection.xml', context, content_type='text/xml')

