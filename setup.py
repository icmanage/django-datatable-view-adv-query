# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='datatableview_advanced_search',
    version='0.1.0',
    description='Django Datatable Advanced Search',
    long_description=readme,
    author='Steven Klasss',
    author_email='sklass@icmanage.com',
    url='https://github.com/icmanage/django-datatable-view-adv-query',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    include_package_data=True,
)

