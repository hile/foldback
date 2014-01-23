#!/usr/bin/env python

import os,glob
from setuptools import setup,find_packages

VERSION='1.0'
README = open(os.path.join(os.path.dirname(__file__),'README.md'),'r').read()

setup(
    name = 'foldback',
    version = VERSION,
    license = 'PSF',
    author = 'Ilkka Tuohela',
    author_email = 'hile@iki.fi',
    description = 'Network monitoring scripts',
    long_description = README,
    keywords = 'nagios network monitoring',
    url = 'http://tuohela.net/packages/foldback',
    zip_safe = False,
    packages = ( 'foldback', 'foldback/nagios' ),
    scripts = glob.glob('bin/*'),
    install_requires = (
        'systematic',
        'seine',
    ),
)

