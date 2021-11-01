from setuptools import setup, find_packages
from os import path
from io import open

# Get current directory and long description from README
current_dir = path.abspath(path.dirname(__file__))

# setup
setup(
    name="MigrationScheduling",
    version="0.1.0",
    description="Load Migration Scheduling",
    author="Matt Buckley",
    packages=find_packages(exclude=['contrib', 'docs', 'tests'])
)
