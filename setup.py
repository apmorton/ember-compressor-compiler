from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()


version = '0.3.0'

install_requires = [
    'PyExecJS',
    'django_compressor'
]

setup(
    name='ember-compressor-compiler',
    version=version,
    description="django_compressor filter to compile ember templates",
    long_description=README,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords='',
    author='Austin Morton',
    author_email='amorton@juvsoft.com',
    url='https://github.com/Juvenal1228/ember-compressor-compiler',
    license='MIT',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={
        'embercompressorcompiler': ['js/*.js'],
    },
    zip_safe=False,
    install_requires=install_requires,
    test_suite='nose.collector'
)
