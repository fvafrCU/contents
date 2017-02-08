# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='contents',
    version='0.3.2',
    description='Exract markdown style comments from a file.',
    author='Andreas Dominik Cullmann',
    author_email='dominik.cullmann@forst.bwl.de',
    url='https://github.com/fvafrcu/contents',
    license='BSD_2_CLAUSE',
    packages=find_packages(exclude=('tests', 'docs', 'output', 'utils'))
)

