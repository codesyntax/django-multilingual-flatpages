# -*- coding: utf-8 -*-
# /usr/bin/env python

import uuid
from setuptools import setup, find_packages
try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

def get_requirements(source):
    try:
        install_reqs = parse_requirements(source, session=uuid.uuid1())
    except TypeError:
        # Older version of pip.
        install_reqs = parse_requirements(source)
    try:
        required = [str(ir.req) for ir in install_reqs]
    except:
        required = [str(ir.requirement) for ir in install_reqs]
    return list(required)

version = '0.8.4'

setup(name='multilingual_flatpages',
      version=version,
      description="""A flatpage is a simple object with a URL, title and content. Use it for one-off, special-case pages, such as “About” or “Privacy Policy” pages, that you want to store in a database but for which you don’t want to develop a custom Django application. A flatpage can use a custom template or a default, systemwide flatpage template. It can be associated with one, or multiple, sites. This version is a fork of django.contrib.flatpages package made it multilingual.""",
      long_description=open("README.rst").read() + "\n" +
                       open("CHANGELOG.txt").read(),
      classifiers=[],
      keywords='',
      author="Urtzi Odriozola (CodeSyntax http://codesyntax.com)",
      author_email="uodriozola@codesyntax.com",
      url="https://github.com/codesyntax/django-multilingual-flatpages",
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=get_requirements('requirements.txt'),
)
