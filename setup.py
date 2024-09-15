# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2024 Anyrta7
#
# You are free to use, modify, and distribute this software under the MPL 2.0 license, with the requirement
# to disclose any modifications to this file. Other files in the project may remain under different licenses.
import subprocess
import sys


def install_missing_packages():
    required_packages = ['setuptools', 'wheel']
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])


install_missing_packages()

from setuptools import setup, find_packages


def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read().splitlines()


setup(
    name='mizper',
    version='0.1.0',
    author='Anyrta7',
    description='(Mirror Scraper) Global Cyber Vandalism Mirror Database Grabber',
    url='https://github.com/anyrta7/Mizper',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=read_file("requirements.txt"),
    entry_points={
        'console_scripts': ['mizper=cli.main:main']
    }
)
