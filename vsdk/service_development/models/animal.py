from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from .vs_element import VoiceServiceElement, VoiceServiceSubElement
from .voicelabel import VoiceLabel

class Animal(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank = True, null = True)
    
    def __str__(self):
        return self.name

   

class Disease(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank = True, null = True)
    related_element = models.ForeignKey(
            VoiceServiceElement, 
            related_name='%(app_label)s_%(class)s_redirect_related',
            blank = True,
            null = True)

    def __str__(self):
        return self.name

    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True

    def validator(self):
        errors = []
        errors.extend(super(SymptomOfDisease, self).validator())
        return errors
    
    @property
    def redirect(self):
        """
        Returns the actual subclassed object that is redirected to,
        instead of the VoiceServiceElement superclass object (which does
        not have specific fields and methods).
        """
        return VoiceServiceElement.objects.get_subclass(id = self.related_element.id)


class DiseaseFragment(models.Model):
    parent = models.ForeignKey('Animal',
            on_delete = models.CASCADE)

    disease = models.ForeignKey(
            'Disease',
            on_delete = models.SET_NULL,
            null = True,
            blank = True
            )
    
    def __str__(self):
        return "Disease Fragment: (%s) %s" % (self.disease.name, self.parent.name)


class AnimalSelection(VoiceServiceElement):
    _urls_name = 'service-development:animal-selection'


    def __str__(self):
        return self.name

    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True

    def validator(self):
        errors = []
        errors.extend(super(AnimalSelection, self).validator())
        return errors
    
    '''@property
    def redirect(self):
        """
        Returns the actual subclassed object that is redirected to,
        instead of the VoiceServiceElement superclass object (which does
        not have specific fields and methods).
        """
        return VoiceServiceElement.objects.get_subclass(id = self._redirect_url.id)'''


class AnimalSelectionOption(VoiceServiceSubElement):
    parent = models.ForeignKey('AnimalSelection',
            on_delete = models.CASCADE,
            related_name='selection_options')

    options = models.ForeignKey(
            'Animal',
            on_delete = models.SET_NULL,
            null = True,
            blank = True
            )
    
    _redirect_url = models.ForeignKey(
            VoiceServiceElement, 
            related_name='%(app_label)s_%(class)s_redirect_related',
            blank = True,
            null = True)

    def __str__(self):
        return "Animal Selection Option: (%s) %s" % (self.options.name, self.parent.name)

    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True

    def validator(self):
        errors = []
        errors.extend(super(AnimalSelectionOption, self).validator())
        return errors
    
    @property
    def redirect(self):
        """
        Returns the actual subclassed object that is redirected to,
        instead of the VoiceServiceElement superclass object (which does
        not have specific fields and methods).
        """
        return VoiceServiceElement.objects.get_subclass(id = self._redirect_url.id)
  
  
