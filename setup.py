# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'auf.fabric',
    'author': 'Olivier Larchevêque',
    'url': 'http://pypi.auf.org/auf.fabric',
    'download_url': 'http://pypi.auf.org/auf.fabric',
    'author_email': 'olivier.larcheveque@auf.org',
    'version': '0.1',
    'install_requires': ['fabric', ],
    'packages': ['auf'],
    'scripts': [],
    'name': 'auf.fabric'
}

setup(**config)
