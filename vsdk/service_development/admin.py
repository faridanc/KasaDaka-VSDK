from django.contrib import admin

from .models import VoiceService, MessagePresentation, Choice, ChoiceOption, VoiceFragment, CallSession, CallSessionStep, KasaDakaUser, Language, VoiceLabel
from .models import Region, RegionSelection, RegionSelectionOption, Animal, Disease, DiseaseFragment, AnimalSelection, AnimalSelectionOption, SymptomOfDisease, Symptom
from .models import Veterinarian, VeterinarianSelection, VeterinarianSelectionOption

def format_validation_result(obj):
        """
        Creates a HTML list from all errors found in validation
        """
        return '<br/>'.join(obj.validator())


class VoiceServiceAdmin(admin.ModelAdmin):
    fieldsets = [('General',    {'fields' : ['name', 'description', 'vxml_url', 'active', 'is_valid', 'validation_details', 'supported_languages']}),
                    ('Requirements', {'fields': ['requires_registration']}),
                    ('Call flow', {'fields': ['_start_element']})]
    list_display = ('name','active','is_valid')
    readonly_fields = ('vxml_url', 'is_valid', 'validation_details')

    def get_readonly_fields(self, request, obj=None):
        """
        Only allow activation of voice service if it is valid
        """
        if obj is not None:
            if not obj.is_valid():
                return self.readonly_fields + ('active',)
        return self.readonly_fields


    def validation_details(self, obj=None):
        return format_validation_result(obj)
    validation_details.allow_tags = True
    

class VoiceServiceElementAdmin(admin.ModelAdmin):
    fieldsets = [('General',    {'fields' : [ 'name', 'description','service','is_valid', 'validation_details', 'voice_label']})]
    list_display = ('name', 'service', 'is_valid')
    readonly_fields = ('is_valid', 'validation_details')
     
    def validation_details(self, obj=None):
        return format_validation_result(obj)
    validation_details.allow_tags = True

class ChoiceOptionsInline(admin.TabularInline):
    model = ChoiceOption
    extra = 2
    fk_name = 'parent'
    view_on_site = False

class ChoiceAdmin(VoiceServiceElementAdmin):
    inlines = [ChoiceOptionsInline]

class VoiceLabelInline(admin.TabularInline):
    model = VoiceFragment
    extra = 2
    fk_name = 'parent'

class VoiceLabelAdmin(admin.ModelAdmin):
    inlines = [VoiceLabelInline]

class CallSessionInline(admin.TabularInline):
    model = CallSessionStep
    extra = 0 
    fk_name = 'session'
    can_delete = False
    fieldsets = [('General', {'fields' : ['visited_element', 'time']})]
    readonly_fields = ('time','session','visited_element')
    max_num = 0

class CallSessionAdmin(admin.ModelAdmin):
    list_display = ('start','user','service','caller_id','language')
    fieldsets = [('General', {'fields' : ['service', 'user','caller_id','start','end','language']})]
    readonly_fields = ('service','user','caller_id','start','end','language') 
    inlines = [CallSessionInline]
    can_delete = False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, reques, obj=None):
        return False

    def get_actions(self, request):
        actions = super(CallSessionAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

class MessagePresentationAdmin(VoiceServiceElementAdmin):
    fieldsets = VoiceServiceElementAdmin.fieldsets + [('Message Presentation', {'fields': ['_redirect','final_element', 'diagnosis_element']})]


'''class RegionAdmin(admin.ModelAdmin):
   fieldsets = [('General',    {'fields' : [ 'name', 'description']})]'''
  
class AnimalInline(admin.TabularInline):
    model = DiseaseFragment
    extra = 2
    fk_name = 'parent'

class AnimalAdmin(admin.ModelAdmin):
  inlines = [AnimalInline]

class AnimalSelectionOptionsInline(admin.TabularInline):
    model = AnimalSelectionOption
    extra = 2
    fk_name = 'parent'
    view_on_site = False

class AnimalSelectionAdmin(VoiceServiceElementAdmin):
    fieldsets = VoiceServiceElementAdmin.fieldsets
    inlines = [AnimalSelectionOptionsInline]

class RegionSelectionOptionsInline(admin.TabularInline):
    model = RegionSelectionOption
    extra = 2
    fk_name = 'parent'
    view_on_site = False

class RegionSelectionAdmin(VoiceServiceElementAdmin):
    fieldsets = VoiceServiceElementAdmin.fieldsets + [('Redirect URL', {'fields': ['_redirect_url']})]
    inlines = [RegionSelectionOptionsInline]

class DiseaseInline(admin.TabularInline):
    model = SymptomOfDisease
    extra = 2
    fk_name = 'disease'
    view_on_site = False

class DiseaseAdmin(admin.ModelAdmin):
  inlines = [DiseaseInline]

class VeterinarianSelectionOptionsInline(admin.TabularInline):
    model = VeterinarianSelectionOption
    extra = 2
    fk_name = 'parent'
    view_on_site = False

class VeterinarianSelectionAdmin(VoiceServiceElementAdmin):
    fieldsets = VoiceServiceElementAdmin.fieldsets + [('Redirect URL', {'fields': ['_redirect_url']})]
    inlines = [VeterinarianSelectionOptionsInline]

# Register your models here.

admin.site.register(VoiceService, VoiceServiceAdmin)
admin.site.register(MessagePresentation, MessagePresentationAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(CallSession, CallSessionAdmin)
admin.site.register(KasaDakaUser)
admin.site.register(Language)
admin.site.register(VoiceLabel, VoiceLabelAdmin)
admin.site.register(Animal, AnimalAdmin)
admin.site.register(Disease, DiseaseAdmin)
#admin.site.register(Region, RegionAdmin)
admin.site.register(Region)
admin.site.register(AnimalSelection, AnimalSelectionAdmin)
admin.site.register(RegionSelection, RegionSelectionAdmin)
admin.site.register(Symptom)
admin.site.register(Veterinarian)
admin.site.register(VeterinarianSelection, VeterinarianSelectionAdmin)
