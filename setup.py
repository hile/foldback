
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
    data_files = [
        ('share/foldback', glob.glob('data/share/*.cfg')),
        ('lib/foldback/agents', glob.glob('data/agents/*')),
        ('lib/foldback/plugins', glob.glob('data/plugins/*')),
    ],
    install_requires = (
        'systematic>=4.4.8',
        'seine>=3.2.0',
        'requests',
        'BeautifulSoup'
    ),
)
