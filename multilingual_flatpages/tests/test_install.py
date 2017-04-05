from django.contrib.sites.models import Site
from django.test import TestCase
from django.utils.translation import activate

try:
    from django.core.urlresolvers import reverse
except ImportError:  # django < 1.10
    from django.urls import reverse
from django.test import Client
from multilingual_flatpages.models import FlatPage
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:  # django < 1.5
    from django.contrib.auth.models import User


class BasicTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            'john',
            'lennon@thebeatles.com',
            'johnpassword')
        self.user.save()
        self.flatpage = FlatPage.objects.language('en').create(
            slug='/en-slug/',
            title='EN Title',
            content='EN Content',
        )
        self.flatpage.sites.add(Site.objects.get(id='1'))
        self.flatpage.save()

    def test_flatpage_view(self):
        activate('en')
        c = Client()
        url = reverse('multilingual_flatpages', args=[self.flatpage.slug])
        response = c.get(url)
        self.assertEqual(response.status_code, 200)
