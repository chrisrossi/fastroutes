import os
from setuptools import setup
from setuptools import find_packages
import sys

VERSION = '0.0'

requires = [
]
tests_require = requires + []

if sys.version < '2.7':
    tests_require += ['unittest2']

testing_extras = tests_require + ['nose', 'coverage', 'tox']
doc_extras = ['Sphinx']

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
except IOError:
    README = CHANGES = ''

setup(name='fastroutes',
      version=VERSION,
      description='Fast Routes',
      long_description=README + '\n\n' + CHANGES,
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=tests_require,
      extras_require={
          'testing': testing_extras,
          'docs': doc_extras,
      },
      test_suite="fastroutes.tests",
      entry_points="""\
      """)
