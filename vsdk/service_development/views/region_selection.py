from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from ..models import *
import datetime


def region_selection_options_resolve_voice_labels(selection_options, language):
    """
    Returns a list of voice labels belonging to the provided list of selection_options.
    """
    selection_options_voice_labels = []
    for selection_option in selection_options:
        selection_options_voice_labels.append(selection_option.get_voice_fragment_url(language))
    return selection_options_voice_labels

def region_selection_generate_context(selection_element, session):
    """
    Returns a dict that can be used to generate the selection VXML template
    selection = this selection element object
    selection_voice_label = the resolved Voice Label URL for this selection element
    selection_options = iterable of selectionOption object belonging to this selection element
    selection_options_voice_labels = list of resolved Voice Label URL's referencing to the selection_options in the same position
    selection_options_redirect_urls = list of resolved redirection URL's referencing to the selection_options in the same position
        """
    selection_options =  selection_element.selection_options.all()
    language = session.language

    month = datetime.datetime.now().month
    if month >=2 & month <=6:
        season = 'dry'
    else:
        season = 'wet'
    
    session.season = season
    session.save()
    redirect_url = selection_element.redirect.get_absolute_url(session)
    
    context = {'selection':selection_element,
                'selection_voice_label':selection_element.get_voice_fragment_url(language),
                'selection_options': selection_options,
                'selection_options_voice_labels': region_selection_options_resolve_voice_labels(selection_options, language),
                'language': language,
                'redirect_url': redirect_url
             }
    return context

def region_selection(request, element_id, session_id):
    selection_element = get_object_or_404(RegionSelection, pk=element_id)
    session = get_object_or_404(CallSession, pk=session_id)
    session.record_step(selection_element)
    context = region_selection_generate_context(selection_element, session)
      
    return render(request, 'region_selection.xml', context, content_type='text/xml')

