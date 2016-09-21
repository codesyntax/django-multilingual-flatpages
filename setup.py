# /usr/bin/env python
import uuid
from setuptools import setup, find_packages
from pip.req import parse_requirements


def get_requirements(source):

    try:
        install_reqs = parse_requirements(source, session=uuid.uuid1())
    except TypeError:
        # Older version of pip.
        install_reqs = parse_requirements(source)
    required = set([str(ir.req) for ir in install_reqs])
    return required

setup(
    name="django-multilingual-flatpages",
    version="1.0",
    description="""A flatpage is a simple object with a URL, title and content. Use it for one-off, special-case pages, such as “About” or “Privacy Policy” pages, that you want to store in a database but for which you don’t want to develop a custom Django application.
    A flatpage can use a custom template or a default, systemwide flatpage template. It can be associated with one, or multiple, sites.""",
    author="Urtzi Odriozola (Code Syntax http://codesyntax.com)",
    author_email="uodriozola@codesyntax.com",
    url="https://github.com/codesyntax/django-multilingual-flatpages",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Environment :: Web Environment',
                 'Framework :: Django',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Topic :: Utilities'],
    install_requires=get_requirements('requirements.txt'),
)
