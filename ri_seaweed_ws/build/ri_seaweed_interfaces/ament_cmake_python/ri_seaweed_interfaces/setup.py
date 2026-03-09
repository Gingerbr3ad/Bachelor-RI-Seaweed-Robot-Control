from setuptools import find_packages
from setuptools import setup

setup(
    name='ri_seaweed_interfaces',
    version='0.0.0',
    packages=find_packages(
        include=('ri_seaweed_interfaces', 'ri_seaweed_interfaces.*')),
)
