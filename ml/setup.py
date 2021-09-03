import setuptools
from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = [
  'setuptools',
  'tensorflow',
  'keras',
  'h5py',
  'cloudstorage',
]

setup(
    name='trainer',
    version='0.1',
    author='Reed Forehand',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    include_package_data=True,
)