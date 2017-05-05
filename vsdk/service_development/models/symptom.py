from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from .voicelabel import VoiceLabel
from .animal import *

class Symptom(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank = True, null = True)

    def __str__(self):
        return self.name 


class SymptomOfDisease(models.Model):        
    disease = models.ForeignKey('Disease',
            on_delete = models.CASCADE,
            related_name='symptom_options')

    symptom = models.ForeignKey(
            'Symptom',
            on_delete = models.SET_NULL,
            null = True,
            blank = True
            )
    element_of_symptom = models.ForeignKey(
            VoiceServiceElement, 
            related_name='%(app_label)s_%(class)s_redirect_related',
            blank = True,
            null = True)

    
    def __str__(self):
        return "Symptom Of Disease: (%s) %s" % (self.disease.name, self.symptom.name)

 
    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True

    def validator(self):
        errors = []
        errors.extend(super(SymptomOfDisease, self).validator())
        return errors
    
    @property
    def related_element(self):
        """
        Returns the actual subclassed object that is redirected to,
        instead of the VoiceServiceElement superclass object (which does
        not have specific fields and methods).
        """
        return VoiceServiceElement.objects.get_subclass(id = self.element_of_symptom.id)
  