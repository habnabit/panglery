from distutils.core import setup

setup(
    name='panglery',
    version='1',

    packages=['panglery', 'panglery.tests'],

    description='event hooks for python',
    author='Aaron Gallagher',
    author_email='_@habnab.it',
    url='https://github.com/habnabit/panglery',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Topic :: Utilities',
    ],
)
