from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from hvad.admin import TranslatableAdmin
from multilingual_flatpages.forms import FlatpageForm
from multilingual_flatpages.models import FlatPage


@admin.register(FlatPage)
class MultiFlatPageAdmin(TranslatableAdmin):

    def get_title(self, obj):
        return obj.safe_translation_getter('title')
    get_title.short_description = _('Title')

    def get_slug(self, obj):
        return obj.safe_translation_getter('slug')
    get_slug.short_description = _('slug')

    form = FlatpageForm
    use_fieldsets = (
        (None, {'fields': ('name', 'slug', 'title', 'content', 'sites')}),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': ('registration_required', 'template_name'),
        }),
    )
    list_display = ('name', 'get_slug', 'get_title', 'all_translations')
    list_filter = ('sites', 'registration_required')
    # search_fields = ('url', 'title')

    def get_fieldsets(self, request, obj=None):
        return self.use_fieldsets
