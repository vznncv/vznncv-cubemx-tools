#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from setuptools import setup, find_packages

project_name = 'vznncv-cubemx-tools'

with open('README.md') as readme_file:
    readme = readme_file.read()
readme = re.sub(r'!\[[^\[\]]*\]\S*', '', readme)

_locals = {}
with open('src/' + project_name.replace('-', '/') + '/_version.py') as fp:
    exec(fp.read(), None, _locals)
__version__ = _locals['__version__']

with open('requirements_dev.txt') as fp:
    test_requirements = fp.read()

setup(
    author="Konstantin Kochin",
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: Software Development :: Internationalization'
    ],
    description="CMake project generator from STM32CubeMX project",
    long_description=readme,
    long_description_content_type="text/markdown",
    url='https://github.com/vznncv/vznncv-cubemx-tools',
    license='MIT',
    include_package_data=True,
    name=project_name,
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'vznncv-cubemx = vznncv.cubemx.tools._cli:main',
        ]
    },
    install_requires=[
        'Jinja2',
        'click'
    ],
    tests_require=test_requirements,
    version=__version__
)
