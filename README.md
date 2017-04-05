# django-multilingual-flatpages

[![Build Status](https://travis-ci.org/codesyntax/django-multilingual-flatpages.svg?branch=master)](https://travis-ci.org/codesyntax/django-multilingual-flatpages) [![Coverage Status](https://coveralls.io/repos/github/codesyntax/django-multilingual-flatpages/badge.svg?branch=master)](https://coveralls.io/github/codesyntax/django-multilingual-flatpages?branch=master) [![Code Health](https://landscape.io/github/codesyntax/django-multilingual-flatpages/master/landscape.svg?style=flat)](https://landscape.io/github/codesyntax/django-multilingual-flatpages/master)


A flatpage is a simple object with a URL, title and content. Use it for one-off, special-case pages, such as “About” or “Privacy Policy” pages, that you want to store in a database but for which you don’t want to develop a custom Django application.

A flatpage can use a custom template or a default, systemwide flatpage template. It can be associated with one, or multiple, sites.

This version is a fork of django.contrib.flatpages package made it multilingual.


## Installation

You will need to uninstall flatpages, and remove all traces of it from the **INSTALLED_APPS**
and **MIDDLEWARES** settings.

To install the multilingual flatpages app, follow these steps:

1. Install this package:

    ```
    $ pip install multilingual_flatpages
    ```

2. Install the sites framework by adding 'django.contrib.sites' to your **INSTALLED_APPS** setting, if it’s not already in there.

3. Also make sure you’ve correctly set **SITE_ID** to the ID of the site the settings file represents. This will usually be **1** (i.e. **SITE_ID = 1**, but if you’re using the sites framework to manage multiple sites, it could be the ID of a different site.

4. Add **'multilingual_flatpages'** and **'hvad'** to your **INSTALLED_APPS** setting.

5. Add **multilingual_flatpages.middleware.FlatpageFallbackMiddleware'** in your **MIDDLEWARES** list.

6. Add a **TINYMCE_DEFAULT_CONFIG** config option in your settings, for example:

    ```python
TINYMCE_DEFAULT_CONFIG = {
    'language': 'en',
    'theme': 'modern',
    'height': 600,
    'plugins': [
        'advlist autolink lists link image charmap print preview anchor',
        'searchreplace visualblocks code fullscreen',
        'insertdatetime media table contextmenu paste',
    ],
    'toolbar': 'styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image media | code preview',
    'menubar': False,
    'media_alt_source': False,
    'media_poster': False,
    'media_dimensions': False,
}```

7. Add an entry in your URLconf. For example:

 ```python
from multilingual_flatpages import views as multilingual_flatpages_views
...
urlpatterns = [
    url(r'^(?P<flatpage_slug>.*)$', multilingual_flatpages_views.flatpage, name='multilingual_flatpages'),
]
```

8. Run the command **manage.py migrate**.


## Getting a URL of FlatPage object in your templates

The flatpages app provides a template tag that allows you to get the absolute url depending on your current language.

Like all custom template tags, you’ll need to load its custom tag library before you can use it. After loading the library, you can retrieve all current flatpages URL via the get_flatpage_url tag:

```python
{% load flatpages %}

{% get_flatpage_url 'flatpage-name' %}
```

You can also use the *get_flatpages* template tag to get all the FlatPages:

```html
{% load flatpages %}

{% get_flatpages as flatpages %}
<ul>
    {% for page in flatpages %}
        <li><a href="{{ page.get_absolute_url }}">{{ page.title }}</a></li>
    {% endfor %}
</ul>
```

## Getting the URL of the translation of a FlatPage in your template

This is useful if you want to provide a language change link:

```html
{% load flatpages %}
{% get_flatpages as flatpages %}
<ul>
    {% for page in flatpages %}
        <li><a href="{% get_translation_url page 'es'%}">{{ page.title }}</a></li>
    {% endfor %}
</ul>
```
