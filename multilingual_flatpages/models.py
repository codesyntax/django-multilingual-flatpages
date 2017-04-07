from __future__ import unicode_literals
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import activate
from django.utils.translation import get_language
from django.utils.translation import ugettext_lazy as _
from hvad.models import TranslatableModel, TranslatedFields


@python_2_unicode_compatible
class FlatPage(TranslatableModel):
    name = models.CharField(_('Name'), max_length=100)
    translations = TranslatedFields(
        slug=models.CharField(_('slug'), max_length=100, db_index=True),
        title=models.CharField(_('title'), max_length=200),
        content=models.TextField(_('content'), blank=True),
    )
    enable_comments = models.BooleanField(_('enable comments'), default=False)
    template_name = models.CharField(
        _('template name'),
        max_length=70,
        blank=True,
        help_text=_(
            "Example: 'multilingual_flatpages/contact_page.html'. If this isn't provided, "
            "the system will use 'multilingual_flatpages/default.html'."
        ),
    )
    registration_required = models.BooleanField(
        _('registration required'),
        help_text=_("If this is checked, only logged-in users will be able to view the page."),
        default=False,
    )
    sites = models.ManyToManyField(Site, verbose_name=_('sites'))

    class Meta:
        app_label = "multilingual_flatpages"
        verbose_name = _('flat page')
        verbose_name_plural = _('flat pages')
        ordering = ('slug',)

    def __str__(self):
        return "%s -- %s" % (self.slug, self.title)

    def get_absolute_url(self):
        # Handle script prefix manually because we bypass reverse()
        if self.slug.startswith("/"):
            slug = self.slug[1:]
        else:
            slug = self.slug
        return reverse('multilingual_flatpages', args=[slug])

    def get_translation_url(self, lang):
        old_lang = get_language()
        activate(lang)
        translation = FlatPage.objects.language(lang).get(id=self.id)
        url = translation.get_absolute_url()
        activate(old_lang)
        return url
