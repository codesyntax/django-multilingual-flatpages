from django.conf.urls import url
from multilingual_flatpages import views

urlpatterns = [
    url(r'^(?P<flatpage_slug>.*)$', views.flatpage, name='multilingual_flatpages'),
]
