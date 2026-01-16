from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.template import loader
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_protect
from multilingual_flatpages.models import FlatPage


DEFAULT_TEMPLATE = 'multilingual_flatpages/default.html'

@csrf_protect
def flatpage(request, flatpage_slug):
    """
    Public interface to the flat page view.
    """
    if not flatpage_slug.startswith('/'):
        flatpage_slug = '/' + flatpage_slug

    site_id = get_current_site(request).id

    try:
        f = get_object_or_404(FlatPage, slug=flatpage_slug, sites=site_id)
    except Http404:
        if settings.APPEND_SLASH and not request.path.endswith('/'):
            # Try appending a slash if it's not there.
            slashed_slug = flatpage_slug + '/'
            try:
                f = get_object_or_404(FlatPage, slug=slashed_slug, sites=site_id)
                return HttpResponsePermanentRedirect(request.path + '/')
            except Http404:
                raise
        else:
            raise

    return render_flatpage(request, f)


def render_flatpage(request, f):
    """
    Internal interface to the flat page view.
    """
    # If registration is required for accessing this page, and the user isn't
    # logged in, redirect to the login page.
    if f.registration_required and not request.user.is_authenticated:
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.path)
    if f.template_name:
        template = loader.select_template((f.template_name, DEFAULT_TEMPLATE))
    else:
        template = loader.get_template(DEFAULT_TEMPLATE)

    # To avoid having to always use the "|safe" filter in flatpage templates,
    # mark the title and content as already safe (since they are raw HTML
    # content in the first place).
    f.title = mark_safe(f.title)
    f.content = mark_safe(f.content)

    response = HttpResponse(template.render({'flatpage': f}, request))
    return response
