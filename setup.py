# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='excerpts',
    version='0.12.2',
    description='Excerpt Markdown Style Comments From a File',
    long_description='Set a table of contents from structuring comments in your script files.',
    author='Andreas Dominik Cullmann',
    author_email='dominik.cullmann@forst.bwl.de',
    url='https://github.com/fvafrcu/excerpts',
    license='BSD',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Documentation',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Operating System :: OS Independent',
    ],
    keywords='sample setuptools development',
    extras_require={
        'test': ['coverage'],
    },
    packages=find_packages(exclude=('tests', 'docs', 'output', 'utils', 'codes_doxygen')),
    entry_points = {
        'console_scripts': ['excerpts=excerpts.command_line:main'],
        }
)

