from setuptools import setup
import os.path

descr_file = os.path.join(os.path.dirname(__file__), 'README.rst')

setup(
    name='panglery',

    packages=['panglery', 'panglery.tests'],
    setup_requires=['vcversioner'],
    vcversioner={
        'version_module_paths': ['panglery/_version.py'],
    },

    description='event hooks for python',
    long_description=open(descr_file).read(),
    author='Aaron Gallagher',
    author_email='_@habnab.it',
    url='https://github.com/habnabit/panglery',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Topic :: Utilities',
    ],
)
