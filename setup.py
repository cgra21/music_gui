from setuptools import setup, find_packages
from pkg_resources import parse_requirements

# Read the requirements from the requirements.txt file
with open('requirements.txt') as f:
    requirements = [str(req) for req in parse_requirements(f)]

setup(
    name='your_package_name',
    version='1.0',
    packages=find_packages(),
    install_requires=requirements,
    author='Cole Granger',
    author_email='cjgranger2001@gmail.com',
    description='This is a basic MIDI gui, it is meant for usage with a model to generate music from text'
)
