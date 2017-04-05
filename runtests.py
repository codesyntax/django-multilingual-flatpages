#!/usr/bin/env python

import sys
import os
import django
from django.conf import settings
from django.test.utils import get_runner


APP_NAME = 'multilingual_flatpages'

if django.VERSION < (1, 10):
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        USE_TZ=True,
        LANGUAGES=(
            ('es', 'Spanish'),
            ('en', 'English'),
        ),
        ROOT_URLCONF='{0}.urls'.format(APP_NAME),
        SITE_ID=1,
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.admin',
            'django.contrib.sites',
            'hvad',
            'tinymce',
            APP_NAME,
        ),
        TEMPLATE_CONTEXT_PROCESSORS=(
            "django.contrib.auth.context_processors.auth",
            "django.core.context_processors.debug",
            "django.core.context_processors.i18n",
            "django.core.context_processors.media",
            "django.core.context_processors.request",
        ),
        MIDDLEWARE_CLASSES=(
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
            'multilingual_flatpages.middleware.FlatpageFallbackMiddleware',
        ),
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
        }
    )
else:
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        USE_TZ=True,
        LANGUAGES=(
            ('es', 'Spanish'),
            ('en', 'English'),
        ),
        ROOT_URLCONF='{0}.urls'.format(APP_NAME),
        SITE_ID=1,
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.admin',
            'django.contrib.sites',
            'hvad',
            'tinymce',
            APP_NAME,
        ),
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [
                    # insert your TEMPLATE_DIRS here
                    os.path.join(os.path.dirname(__file__), "templates"),
                ],
                'OPTIONS': {
                    'context_processors': [
                        # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                        # list if you haven't customized them:
                        "django.contrib.auth.context_processors.auth",
                        "django.template.context_processors.debug",
                        "django.template.context_processors.i18n",
                        "django.template.context_processors.media",
                        "django.template.context_processors.request",
                    ],
                    'loaders': [
                        # insert your TEMPLATE_LOADERS here
                        'django.template.loaders.filesystem.Loader',
                        'django.template.loaders.app_directories.Loader',
                    ]
                },
            },
        ],
        MIDDLEWARE=[
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
            'multilingual_flatpages.middleware.FlatpageFallbackMiddleware',
        ],
        TINYMCE_DEFAULT_CONFIG={
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
        }
    )

if hasattr(django, 'setup'):
    django.setup()
TestRunner = get_runner(settings)
test_runner = TestRunner()
failures = test_runner.run_tests([APP_NAME])
if failures:
    sys.exit(failures)
