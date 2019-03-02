from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = [
  'tensorflow',
  'keras',
  'h5py',
]

setup(
    name='trainer',
    version='0.1',
    author='Reed Forehand',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    include_package_data=True,
)