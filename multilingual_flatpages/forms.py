from django import forms
from django.conf import settings
from django.utils.translation import ugettext, ugettext_lazy as _
from hvad.forms import TranslatableModelForm
from multilingual_flatpages.models import FlatPage
from tinymce.widgets import TinyMCE


class FlatpageForm(TranslatableModelForm):
    slug = forms.RegexField(
        label=_("slug"),
        max_length=100,
        regex=r'^[-\w/\.~]+$',
        help_text=_("Example: '/about/contact/'. Make sure to have leading and trailing slashes."),
        error_messages={
            "invalid": _(
                "This value must contain only letters, numbers, dots, "
                "underscores, dashes, slashes or tildes."
            ),
        },
    )
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}, mce_attrs=settings.TINYMCE_DEFAULT_CONFIG))

    class Meta:
        model = FlatPage
        # fields = '__all__'

    def clean_url(self):
        slug = self.cleaned_data['slug']
        if not slug.startswith('/'):
            raise forms.ValidationError(
                ugettext("URL is missing a leading slash."),
                code='missing_leading_slash',
            )
        if (settings.APPEND_SLASH and (
                'django.middleware.common.CommonMiddleware' in settings.MIDDLEWARE_CLASSES) and
                not slug.endswith('/')):
            raise forms.ValidationError(
                ugettext("URL is missing a trailing slash."),
                code='missing_trailing_slash',
            )
        return slug

    def clean(self):
        slug = self.cleaned_data.get('slug')
        sites = self.cleaned_data.get('sites')

        same_url = FlatPage.objects.language().filter(slug=slug)
        if self.instance.pk:
            same_url = same_url.exclude(pk=self.instance.pk)

        if sites and same_url.filter(sites__in=sites).exists():
            for site in sites:
                if same_url.filter(sites=site).exists():
                    raise forms.ValidationError(
                        _('Flatpage with url %(url)s already exists for site %(site)s'),
                        code='duplicate_url',
                        params={'slug': slug, 'site': site},
                    )

        return super(FlatpageForm, self).clean()
