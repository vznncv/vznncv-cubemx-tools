#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages

project_name = 'vznncv-cubemx-tools'

with open('README.md') as readme_file:
    readme = readme_file.read()

_locals = {}
with open('src/' + project_name.replace('-', '/') + '/_version.py') as fp:
    exec(fp.read(), None, _locals)
__version__ = _locals['__version__']

requirements = [
    'Jinja2',
    'click'
]

with open('requirements_dev.txt') as fp:
    test_requirements = fp.read()

setup(
    author="Konstantin Kochin",
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    description=readme,
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
    install_requires=requirements,
    tests_require=test_requirements,
    version=__version__
)
