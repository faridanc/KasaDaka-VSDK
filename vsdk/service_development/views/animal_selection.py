from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django import template

from ..models import *
import datetime


register = template.Library()
@register.filter
def get_at_index(list, index):
    return list[index]

def animal_selection_resolve_redirect_urls(selection_options, session):
    selection_options_redirection_urls = []
    for selection_option in selection_options:
        redirect_url = selection_option.redirect.get_absolute_url(session)
        option_id = selection_option.options_id
        selection_options_redirection_urls.append([option_id, redirect_url])
    return selection_options_redirection_urls

def animal_selection_options_resolve_voice_labels(selection_options, language):
    """
    Returns a list of voice labels belonging to the provided list of selection_options.
    """
    selection_options_voice_labels = []
    for selection_option in selection_options:
        selection_options_voice_labels.append(selection_option.get_voice_fragment_url(language))
    return selection_options_voice_labels

def animal_selection_generate_context(selection_element, session):
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
    
    context = {'selection':selection_element,
                'selection_voice_label':selection_element.get_voice_fragment_url(language),
                'selection_options': selection_options,
                'selection_options_voice_labels': animal_selection_options_resolve_voice_labels(selection_options, language),
                'language': language,
                'selection_options_redirect_urls': animal_selection_resolve_redirect_urls(selection_options,session),
                    }
    return context

def animal_selection(request, element_id, session_id):
    
    selection_element = get_object_or_404(AnimalSelection, pk=element_id)
    session = get_object_or_404(CallSession, pk=session_id)
    session.record_step(selection_element)
    
    if request.method == "POST" and request.POST['region_id']:
        region_id = request.POST['region_id']
        session.region = region_id
        session.save()

    context = animal_selection_generate_context(selection_element, session)  
    
    return render(request, 'animal_selection.xml', context, content_type='text/xml')

