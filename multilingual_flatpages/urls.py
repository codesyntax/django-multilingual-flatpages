from django.conf.urls import url
from multilingual_flatpages import views

urlpatterns = [
    url(r'^(?P<url>.*)$', views.flatpage, name='multilingual_flatpages'),
]
