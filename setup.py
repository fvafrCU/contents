# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='excerpts',
    version='0.9.0',
    description='Exract markdown style comments from a file.',
    author='Andreas Dominik Cullmann',
    author_email='dominik.cullmann@forst.bwl.de',
    url='https://github.com/fvafrcu/excerpts',
    license='BSD_2_CLAUSE',
    packages=find_packages(exclude=('tests', 'docs', 'output', 'utils')),
        entry_points = {
        'console_scripts': ['excerpts=excerpts.command_line:main'],
    }
)

