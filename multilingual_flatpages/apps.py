from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FlatPagesConfig(AppConfig):
    name = 'multilingual_flatpages'
    verbose_name = _("Multilingual Flat Pages")
