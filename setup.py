from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()


version = '0.1'

install_requires = [
    'PyExecJS',
    'django_compressor'
]

tests_require = [
    'Django'
]

setup(name='ember-compressor-compiler',
    version=version,
    description="django_compressor filter to compile ember templates",
    long_description=README,
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='',
    author='Austin Morton',
    author_email='amorton@juvsoft.com',
    url='',
    license='MIT',
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data=True,
    package_data = {
        'embercompressorcompiler': ['js/*.js'],
    },
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    test_suite='nose.collector'
)
