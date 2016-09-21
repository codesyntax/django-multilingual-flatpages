from django.contrib import admin
from multilingual_flatpages.forms import FlatpageForm
from multilingual_flatpages.models import FlatPage
from django.utils.translation import ugettext_lazy as _
from hvad.admin import TranslatableAdmin


@admin.register(FlatPage)
class FlatPageAdmin(TranslatableAdmin):

    def get_title(self, obj):
        return obj.safe_translation_getter('title')
    get_title.short_description = _('Title')

    form = FlatpageForm
    use_fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': ('registration_required', 'template_name'),
        }),
    )
    list_display = ('url', 'get_title')
    list_filter = ('sites', 'registration_required')
    # search_fields = ('url', 'title')

    def get_fieldsets(self, request, obj=None):
        return self.use_fieldsets
