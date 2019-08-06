"""
Zenaton client library
"""
from __future__ import absolute_import, print_function, unicode_literals

import os
from io import open

from setuptools import find_packages, setup

import zenaton


def read(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, encoding='utf-8') as f:
        return f.read()

TEST_DEPS = [
    'freezegun',
    'pytest',
    'pytest_mock',
    'python-dotenv',
]

setup(
    name='zenaton',
    version=zenaton.__version__,
    author='Zenaton',
    author_email='yann@zenaton.com',
    description='Zenaton client library',
    long_description=read('README.md') + '\n' + read('CHANGELOG.md'),
    long_description_content_type='text/markdown',
    keywords=['workflow engine', 'workflows', 'orchestration', 'event-driven architecture', 'queuing systems', 'orchestration engine', 'background jobs', 'hosted queues', 'queues', 'jobs', 'asynchronous tasks'],
    url='https://zenaton.com/',
    license='Apache License, Version 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3',
    install_requires=[
        'requests',
        'pytz'
    ],
    tests_require=TEST_DEPS,
    extras_require={'test': TEST_DEPS},
    zip_safe=False
)
