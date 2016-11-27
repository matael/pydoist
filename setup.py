#! /usr/bin/env python

from setuptools import setup

long_description="""
This package provides a very basic interface to Todoist.

The Pydoist class allows parsing of strings list as Todoist entries, extracting the needed
information from the string itself and bundling it into an item.

It **does require** a Todoist account and an API token to work. The token can be set at
runtime using the ``--token`` parameter of ``pydoist`` or from the
``~/.config/pydoist.conf`` file (which may contain only the token). 

The project names inference uses Levenshtein distance.
In the default script with the default markers, one may use :

- ``%%i`` with ``i`` a number to set priority
- ``@datestr`` to perform date inference on ``datestr``
- ``#projectname`` for project inference on ``projectname``
"""

setup(name='Pydoist',
      version='1.0',
      description='Todoist integration script utility',
      author='Mathieu (matael) Gaborit',
      author_email='mathieu@matael.org',
      url='https://github.com/Matael/pydoist',
      packages = ['pydoist'],
      package_dir={'pydoist': 'lib'},
      scripts=['scripts/pydoist'],
      long_description=long_description,
      classifiers=[
          'Programming Language :: Python :: 3',
          'Operating System :: OS Independent',
          ],
      license ='WTFPL',
      install_requires=[
          'todoist-python>=7.0.0',
          'python-Levenshtein>=0.12.0',
          ],
      dependency_links=[
          'git+https://github.com/Doist/todoist-python#egg=todoist-7.0',
          ]
    )
