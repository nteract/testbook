#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""
setup.py

See:
https://packaging.python.org/tutorials/packaging-projects/
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject

"""
import os
from setuptools import setup


local_path = os.path.dirname(__file__)
# Fix for tox which manipulates execution pathing
if not local_path:
    local_path = '.'
here = os.path.abspath(local_path)


def version():
    with open(here + '/testbook/_version.py', 'r') as ver:
        for line in ver.readlines():
            if line.startswith('version ='):
                return line.split(' = ')[-1].strip()[1:-1]
    raise ValueError('No version found in testbook/version.py')


def read(fname):
    with open(fname, 'r') as fhandle:
        return fhandle.read()


def read_reqs(fname):
    req_path = os.path.join(here, fname)
    return [req.strip() for req in read(req_path).splitlines() if req.strip()]


# Get the long description from the README file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='testbook',
    version=version(),
    description='TODO',
    author='nteract contributors',
    author_email='nteract@googlegroups.com',
    license='BSD',
    # Note that this is a string of words separated by whitespace, not a list.
    keywords='jupyter mapreduce nteract pipeline notebook',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nteract/testbook',
    packages=['testbook'],
    python_requires='>=3.5',
    install_requires=read_reqs('requirements.txt'),
    project_urls={
        'Documentation': 'https://testbook.readthedocs.io',
        'Funding': 'https://nteract.io',
        'Source': 'https://github.com/nteract/testbook/',
        'Tracker': 'https://github.com/nteract/testbook/issues',
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
