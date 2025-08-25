from setuptools import setup, find_packages

setup(
    name='apptio_lib',
    version='1.0.0',
    packages=find_packages(),
    description='A collection of internal helper functions for Cloudability, Frontdoor, TBM Studio, and other Apptio applications.',
    author='Jeff Corder',
    author_email='jeff.corder@ibm.com',
    install_requires=[
        'requests',
    ],
)