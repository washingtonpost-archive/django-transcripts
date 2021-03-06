#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import transcription

setup(
        name='django-transcripts',
        version=transcription.__version__,
        description='A reusable Django app for scraping, storing and categorizing political speech.',
        author=transcription.__author__,
        author_email=['bowersj@washpost.com'],
        url='https://github.com/washingtonpost/django-transcripts',
        packages=[
            'transcription'
        ],
        install_requires=[
            'beautifulsoup4',
            'requests',
            'Django>=1.3',
            'django-tastypie',
            'south',
        ],
        license=transcription.__license__,
        classifiers=[
            'Environment :: Web Environment',
            'Framework :: Django',
            'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Utilities'
        ],
)