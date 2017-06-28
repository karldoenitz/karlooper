#!/usr/bin/env python
import platform
from setuptools import setup, Extension
from karlooper import __version__

with open('requirements.txt') as f:
    required = f.read().splitlines()

kwargs = {}
if platform.python_implementation() == 'CPython':
    kwargs['ext_modules'] = [
        Extension(
            'karlooper.utils.encryption',
            sources=['karlooper/utils/encryption.c'],
            extra_compile_args=["-Wno-char-subscripts"]
        ),
    ]

setup(
    name='karlooper',
    version=__version__,
    install_requires=required,
    packages=[
        'karlooper',
        'karlooper.autoreload',
        'karlooper.config',
        'karlooper.escape',
        'karlooper.http_parser',
        'karlooper.logger',
        'karlooper.router',
        'karlooper.template',
        'karlooper.utils',
        'karlooper.web'
    ],
    data_files=[
        ('karlooper/logger', ['karlooper/logger/log.conf']),
        ('karlooper/logger', ['karlooper/logger/log.conf']),
        ('lib/python2.7/dist-packages/karlooper/logger', ['karlooper/logger/log.conf']),
        ('lib/python2.7/site-packages/karlooper/logger', ['karlooper/logger/log.conf'])
    ],
    url='https://github.com/karldoenitz/karlooper',
    license='',
    author='lizhihao',
    author_email='karlvorndoenitz@gmail.com',
    description='karloop plus framework',
    long_description=open("README.rst").read(),
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],
    **kwargs
)
