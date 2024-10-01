from codecs import open

"""
This script sets up the what3words Python API wrapper library.

It reads the version from the version.py file, the requirements from the requirements.txt file,
and the long description from the README.md file. It then uses setuptools to package the library.

Attributes:
    version (dict): A dictionary to store the version information read from version.py.
    requires (list): A list of dependencies read from requirements.txt.
    long_description (str): The content of the README.md file used as the long description.

Functions:
    setup(): Configures the package using setuptools.
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import os

# Read the version from version.py
version = {}
version_file_path = os.path.join(os.path.dirname(__file__), "what3words", "version.py")
with open(version_file_path) as fp:
    exec(fp.read(), version)

with open("requirements.txt") as f:
    requires = f.read().splitlines()

# Read the contents of the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="what3words",
    version=version["__version__"],
    author="what3words",
    author_email="support@what3words.com",
    url="https://github.com/what3words/w3w-python-wrapper",
    description="what3words Python API wrapper library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=["what3words"],
    package_dir={"what3words": "what3words"},
    install_requires=requires,
    keywords="what3words geocoder",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries",
    ],
)
