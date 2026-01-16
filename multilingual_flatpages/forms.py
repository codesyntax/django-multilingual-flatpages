from django import forms
from django.conf import settings
from django.utils.translation import gettext, gettext_lazy as _
from multilingual_flatpages.models import FlatPage
from tinymce.widgets import TinyMCE


class FlatpageForm(forms.ModelForm):
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
        fields = '__all__'

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if not slug.startswith('/'):
            raise forms.ValidationError(
                gettext("URL is missing a leading slash."),
                code='missing_leading_slash',
            )
        middleware = []
        # Support old and new middleware settings names
        middleware += list(getattr(settings, 'MIDDLEWARE', []))
        middleware += list(getattr(settings, 'MIDDLEWARE_CLASSES', []))

        if (settings.APPEND_SLASH and (
            'django.middleware.common.CommonMiddleware' in middleware) and
            not slug.endswith('/')):
            raise forms.ValidationError(
                gettext("URL is missing a trailing slash."),
                code='missing_trailing_slash',
            )
        return slug

    def clean(self):
        slug = self.cleaned_data.get('slug')
        sites = self.cleaned_data.get('sites')

        same_url = FlatPage.objects.filter(slug=slug)
        if self.instance.pk:
            same_url = same_url.exclude(pk=self.instance.pk)

        if sites and same_url.filter(sites__in=sites).exists():
            for site in sites:
                if same_url.filter(sites=site).exists():
                    raise forms.ValidationError(
                        _('A flatpage with url %(slug)s already exists for site %(site)s.'),
                        code='duplicate_slug',
                        params={'slug': slug, 'site': site},
                    )
        return self.cleaned_data
