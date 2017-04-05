from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.template import loader
from django.utils.safestring import mark_safe
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_protect
from multilingual_flatpages.models import FlatPage


DEFAULT_TEMPLATE = 'multilingual_flatpages/default.html'

# This view is called from FlatpageFallbackMiddleware.process_response
# when a 404 is raised, which often means CsrfViewMiddleware.process_view
# has not been called even if CsrfViewMiddleware is installed. So we need
# to use @csrf_protect, in case the template needs {% csrf_token %}.
# However, we can't just wrap this view; if no matching flatpage exists,
# or a redirect is required for authentication, the 404 needs to be returned
# without any CSRF checks. Therefore, we only
# CSRF protect the internal implementation.


def flatpage(request, flatpage_slug):
    """
    Public interface to the flat page view.

    Models: `flatpages.flatpages`
    Templates: Uses the template defined by the ``template_name`` field,
        or :template:`flatpages/default.html` if template_name is not defined.
    Context:
        flatpage
            `flatpages.flatpages` object
    """
    if not flatpage_slug.startswith('/'):
        flatpage_slug = '/' + flatpage_slug
    site_id = get_current_site(request).id
    try:
        f = FlatPage.objects.language(get_language()).get(slug=flatpage_slug, sites=site_id)
    except:
        if not flatpage_slug.endswith('/') and settings.APPEND_SLASH:
            flatpage_slug += '/'
            try:
                f = FlatPage.objects.language(get_language()).get(slug=flatpage_slug, sites=site_id)
            except:
                raise Http404
            return HttpResponsePermanentRedirect('%s/' % request.path)
        else:
            raise Http404
    return render_flatpage(request, f)


@csrf_protect
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

    response = HttpResponse(template.render({'obj': f}, request))
    return response
