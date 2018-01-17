#!/usr/bin/env python
import os
import platform
from setuptools import setup, Extension
from karlooper import __version__

# load requirements file
requirements = 'requirements.txt'
if os.path.exists(requirements):
    with open(requirements) as f:
        required = f.read().splitlines()
else:
    with open('karlooper.egg-info/requires.txt') as f:
        required = f.read().splitlines()

# whether need add c extension
kwargs = {}
if platform.python_implementation() == 'CPython' and platform.system().lower() not in ['windows']:
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
        'karlooper.coroutine',
        'karlooper.escape',
        'karlooper.http_parser',
        'karlooper.logger',
        'karlooper.router',
        'karlooper.template',
        'karlooper.utils',
        'karlooper.web'
    ],
    package_data={
        '': ['*.txt', '*.pyi', '*.conf']
    },
    url='https://github.com/karldoenitz/karlooper',
    license='MIT',
    author='lizhihao',
    author_email='karlvorndoenitz@gmail.com',
    description='karloop plus micro-framework',
    long_description=open("README.rst").read(),
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5'
    ],
    **kwargs
)
