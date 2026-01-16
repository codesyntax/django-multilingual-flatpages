from django.urls import re_path
from multilingual_flatpages import views

urlpatterns = [
    re_path(r'^(?P<flatpage_slug>.*)$', views.flatpage, name='multilingual_flatpages'),
]
