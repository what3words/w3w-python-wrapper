from setuptools import setup, find_packages

from what3words import __version__


setup(
    name='what3words',
    version='.'.join([str(x) for x in __version__]),
    author='What3Words',
    author_email='support@what3words.com',
    url='https://github.com/what3words/w3w-python-wrapper',
    description='What3words API library',
    license='MIT',
    packages=find_packages(),
    install_requires=['six'],
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
