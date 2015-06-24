# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

requirements = open('requirements.txt', 'r')
requirements = requirements.readlines()

setup(
    name='SisComando',
    version='0.2.1',
    author='SisComando Team',
    author_email='horacioibrahim@gmail.com',
    packages=find_packages('siscomando'),
    package_dir={'': 'siscomando'},
    url='https://github.com/siscomando',
    download_url='https://github.com/siscomando/webapp/tarball/master',
    description='Web app of the Siscomando',
    install_requires=requirements,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
  ],
  keywords=['siscomando', 'polymer']
)
