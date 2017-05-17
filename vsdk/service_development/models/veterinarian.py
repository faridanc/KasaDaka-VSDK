from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from .vs_element import VoiceServiceElement, VoiceServiceSubElement
from .voicelabel import VoiceLabel
from .region import *

class Veterinarian(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank = True, null = True)
    phone_number = models.CharField('phone number',max_length=100)
    region = models.ForeignKey(
            Region,
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            )
     
    def __str__(self):
        return self.name

class VeterinarianSelection(VoiceServiceElement):
    _urls_name = 'service-development:veterinarian-selection'
    _redirect_url = models.ForeignKey(
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
        errors.extend(super(VeterinarianSelection, self).validator())
        return errors

    @property
    def redirect(self):
        """
        Returns the actual subclassed object that is redirected to,
        instead of the VoiceServiceElement superclass object (which does
        not have specific fields and methods).
        """
        return VoiceServiceElement.objects.get_subclass(id = self._redirect_url.id)

class VeterinarianSelectionOption(VoiceServiceSubElement):
    parent = models.ForeignKey('VeterinarianSelection',
            on_delete = models.CASCADE,
            related_name='selection_options')

    options = models.ForeignKey(
            'Veterinarian',
            on_delete = models.SET_NULL,
            null = True,
            blank = True
            )
    
    def __str__(self):
        return "Veterinarian Selection Option: (%s) %s" % (self.options.name, self.parent.name)

    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True

    def validator(self):
        errors = []
        errors.extend(super(ChoiceOption, self).validator())
        return errors