# ----------------------------------------------------------------------
# setup.py -- tksapi setup script
#
# Copyright (C) 2017, TickSmith Corp.
# ----------------------------------------------------------------------


from setuptools import find_packages, setup
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))


def read(*parts):
    with open(path.join(here,*parts), encoding='utf-8') as f:
        return f.read()


def main():
    setup_options = {
        "name": "tickvault-python-api",
        "version": "1.2.0",
        "description": "TickVault Python Query API",
        "long_description": read("README.md"),
        "author": "TickSmith Corp.",
        "author_email": "support@ticksmith.com",
        "url": "https://github.com/ticksmith/tickvault-python-api",
        "license": "MIT",
        "install_requires": ['requests', 'ujson', 'numpy', 'pandas', 'pyparsing'],
        "packages": find_packages(),
        "data_files": [('', ['LICENSE.txt'])],
        "platforms": ["any"],
        "zip_safe": True,
        "keywords": "tickvault python api client",
        "classifiers": [
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: Financial and Insurance Industry',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Topic :: Software Development',
            'Topic :: Software Development :: Libraries'
        ]
    }

    # Run the setup
    setup(**setup_options)

if __name__ == '__main__':
    main()
