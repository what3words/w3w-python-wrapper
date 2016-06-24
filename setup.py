from codecs import open
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = ''
with open('what3words/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

requires = ['unirest']

setup(
    name='what3words',
    version=version,
    author='What3Words',
    author_email='support@what3words.com',
    url='https://github.com/what3words/w3w-python-wrapper',
    description='What3words API wrapper library',
    license='MIT',
    packages=['what3words'],
    package_dir={'what3words': 'what3words'},
    install_requires=requires,
    keywords='what3words geocoder',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries',
    ),
)
