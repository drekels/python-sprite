#!/usr/bin/env python


from distutils.core import setup
import os.path


req_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "requirements.txt")
with open('requirements.txt') as f:
    required = f.read().splitlines()


import sprite
version = sprite.get_version()


setup(
    name='python-sprite',
    version=version,
    description="Python Sprite Library",
    author='Kevin Steffler',
    author_email='kevin5steffler@gmail.com',
    url='https://github.com/drekels/python-sprite',
    packages=['sprite'],
    install_requires=required,
)
