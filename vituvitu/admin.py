from django.contrib import admin

from django.contrib.flatpages.models import FlatPage

from django import forms

# Note: we are renaming the original Admin and Form as we import them!
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld
from django.contrib.flatpages.admin import FlatpageForm as FlatpageFormOld

from ckeditor.widgets import CKEditorWidget

from .models import *

class FlatpageForm(FlatpageFormOld): #, TranslationModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta(FlatpageFormOld.Meta):
        pass


class FlatPageAdmin(FlatPageAdminOld): #, TranslationAdmin):
    form = FlatpageForm


class SlugTitleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


# We have to unregister the normal admin, and then reregister ours
admin.site.register(Contact)
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)

