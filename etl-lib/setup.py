# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="transformation",
    version="0.0.1",
    description="Data transformation library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    author="Brenda Kao",
    author_email="bkao000@gmail.com",
    license="",
    classifiers=[
        "Intended Audience :: Test Reviewer",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    packages=["transformation"],
    include_package_data=True,
)


