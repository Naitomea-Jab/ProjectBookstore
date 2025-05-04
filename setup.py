# setup.py

from setuptools import setup, find_packages

setup(
    name='ProjectBookstore',
    version='0.1',
    description='Moduł księgarni e-book, projekt szkolny',
    author='Kacper Jabłoński',
    packages=find_packages(),
    install_requires=[
        'python-dateutil>=2.9.0.post0',
    ],
)