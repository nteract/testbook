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


long_description = read(os.path.join(os.path.dirname(__file__), "README.md"))
requirements = read(os.path.join(os.path.dirname(__file__), "requirements.txt"))
dev_reqs = read_reqs(os.path.join(os.path.dirname(__file__), 'requirements-dev.txt'))
doc_reqs = read_reqs(os.path.join(os.path.dirname(__file__), 'docs/requirements-doc.txt'))
extras_require = {"test": dev_reqs, "dev": dev_reqs, "sphinx": doc_reqs}

setup(
    name='nteract-testbook',
    version=version(),
    description='A unit testing framework for Jupyter Notebooks',
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
    install_requires=requirements,
    extras_require=extras_require,
    project_urls={
        'Documentation': 'https://test-book.readthedocs.io',
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
