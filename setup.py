#!/usr/bin/env python

import sys
import os
import glob

from setuptools import setup, find_packages
from foldback import __version__

setup(
    name = 'foldback',
    version = __version__,
    license = 'PSF',
    author = 'Ilkka Tuohela',
    author_email = 'hile@iki.fi',
    description = 'Network/System monitoring plugins for nagios',
    keywords = 'nagios network monitoring',
    url = 'http://tuohela.net/packages/foldback',
    packages = find_packages(),
    scripts = glob.glob('bin/*'),
    data_files = [
        ('data/etc/foldback', glob.glob('data/config/*.cfg')),
        ('data/lib/foldback/plugins', glob.glob('data/plugins/*')),
    ],
    install_requires = (
        'systematic>=4.4.0',
        'seine>=3.1.0',
        'requests',
        'BeautifulSoup'
    ),
)

