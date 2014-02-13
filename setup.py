#!/usr/bin/env python

import sys
import os
import glob

from setuptools import setup, find_packages

VERSION='1.1'
README = open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r').read()

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
    data_files = [
        ('data/etc/foldback', glob.glob('data/config/*.cfg')),
        ('data/lib/foldback/plugins', glob.glob('data/plugins/*')),
    ],
    install_requires = (
        'systematic>=4.0.2',
        'seine>=2.2',
        'requests',
        'BeautifulSoup'
    ),
)

