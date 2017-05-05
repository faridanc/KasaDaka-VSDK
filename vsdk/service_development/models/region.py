from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from .vs_element import VoiceServiceElement, VoiceServiceSubElement
from .voicelabel import VoiceLabel

class Region(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank = True, null = True)
    voice_label = models.ForeignKey(
            VoiceLabel,
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            )
     
    def __str__(self):
        return self.name


from django.db import models


class RegionSelection(VoiceServiceElement):
    _urls_name = 'service-development:region-selection'
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
        errors.extend(super(RegionSelection, self).validator())
        return errors

    @property
    def redirect(self):
        """
        Returns the actual subclassed object that is redirected to,
        instead of the VoiceServiceElement superclass object (which does
        not have specific fields and methods).
        """
        return VoiceServiceElement.objects.get_subclass(id = self._redirect_url.id)

class RegionSelectionOption(VoiceServiceSubElement):
    parent = models.ForeignKey('RegionSelection',
            on_delete = models.CASCADE,
            related_name='selection_options')

    options = models.ForeignKey(
            'Region',
            on_delete = models.SET_NULL,
            null = True,
            blank = True
            )
    
    def __str__(self):
        return "Region Selection Option: (%s) %s" % (self.options.name, self.parent.name)

    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True

    def validator(self):
        errors = []
        errors.extend(super(ChoiceOption, self).validator())
        return errors

