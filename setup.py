"""A setuptools based setup module for omnisci renderers"""
# To use a consistent encoding
from codecs import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="jupyter-immerse",
    version="0.1.0",
    description="Immerse proxy for the jupyter notebook server",
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    install_requires=[
        "notebook"
    ]
)
