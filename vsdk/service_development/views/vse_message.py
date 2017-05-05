from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from ..models import *

def message_presentation_get_redirect_url(message_presentation_element,session):
    if not message_presentation_element.final_element:
        return message_presentation_element.redirect.get_absolute_url(session)
    else:
        return None
    
def message_presentation_get_diagnosis(message_presentation_element,session):
    if message_presentation_element.diagnosis_element:
        return get_disease_diagnosis(session)
    else:
        return None

def message_presentation_generate_context(message_presentation_element,session):
    language = session.language
    message_voice_fragment_url = message_presentation_element.get_voice_fragment_url(language)
    redirect_url = message_presentation_get_redirect_url(message_presentation_element,session) 
    outcomes = message_presentation_get_diagnosis(message_presentation_element,session) 
    if outcomes:
        redirect_url = outcomes
    context = {'message_voice_fragment_url':message_voice_fragment_url,
            'redirect_url':redirect_url,
            'outcomes' : outcomes}
    return context


def message_presentation(request, element_id, session_id):
    message_presentation_element = get_object_or_404(MessagePresentation, pk=element_id)
    session = get_object_or_404(CallSession, pk=session_id)
    session.record_step(message_presentation_element)

    if request.method == "POST" and request.POST.get('answer_', ''):
        element_symptom_id = request.POST['curr_element_id']
        try:
            symptom = get_list_or_404(SymptomOfDisease, element_of_symptom_id=element_symptom_id)
            session.record_answer(request.POST['answer_'], element_symptom_id, symptom[0].symptom_id)
        except:
                None
        
    context = message_presentation_generate_context(message_presentation_element, session)
    
    return render(request, 'message_presentation.xml', context, content_type='text/xml')

def get_disease_diagnosis(session):
    session_id = session.id
    detected_symptom_list = CallAnswerList.objects.filter(session_id=session_id, answer='1').values_list('symptom_id', flat=True)
    diagnosed_disease_id= None
    if detected_symptom_list:
        all_diseases = Disease.objects.all().values('id').values_list('id', flat=True)
        
        for disease in all_diseases:
            symptoms_per_disease = SymptomOfDisease.objects.filter(disease_id=disease).values_list('symptom_id', flat=True)
            if set(symptoms_per_disease) == set(detected_symptom_list):
                diagnosed_disease_id = disease
                break

        if not diagnosed_disease_id:
            return None
        else:
            related_disease_element = get_object_or_404(Disease, id=diagnosed_disease_id)
            return related_disease_element.redirect.get_absolute_url(session)
