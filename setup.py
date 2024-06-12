from setuptools import setup, find_packages

setup(
    name='Proxy',
    version='0.5',
    packages=find_packages(),
    description='A simple proxy module',
    install_requires=[
        'requests',
        'aiohttp'
    ],
)