# -*- coding: utf-8 -*-
try:
	from distutils.core import setup
except ImportError:
	from setuptools import setup


setup(
    name='siscomando',
    version='0.2.0',
    author='Horacio Ibrahim',
    author_email='horacioibrahim@gmail.com',
    packages=['siscomando'],
    url='https://github.com/siscomando',
    download_url='https://github.com/siscomando/webapp/tarball/master',
    description='Web app of the Siscomando',
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