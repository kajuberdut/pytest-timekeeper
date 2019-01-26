import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="pytest-timekeeper",
    version="0.0.1",
    author="Patrick Shechet",
    author_email="patrick.shechet@gmail.com",
    description=("Pytest timeing framework"),
    license="BSD",
    packages=find_packages(),
    long_description=read("README.md"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Framework :: Pytest",
    ],  # the following makes a plugin available to pytest
    entry_points={"pytest11": ["timekeeper = pytest_timekeeper.plugin"]},
)
