from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TabbedTranslationAdmin
from multilingual_flatpages.models import FlatPage
from tinymce.widgets import TinyMCE


@admin.register(FlatPage)
class MultiFlatPageAdmin(TabbedTranslationAdmin):
    group_fieldsets = True

    fieldsets = (
        (None, {'fields': ('name', 'title', 'slug', 'content', 'sites')}),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': ('registration_required', 'template_name'),
        }),
    )

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE},
    }

    list_display = ('name', 'slug', 'title')
    list_filter = ('sites', 'registration_required')

    class Media:
        js = (
            "extra/js/jquery-ui.min.js",
            "modeltranslation/js/force_jquery.js",
            "modeltranslation/js/tabbed_translation_fields.js",
        )
        css = {
            "screen": ("modeltranslation/css/tabbed_translation_fields.css",),
        }