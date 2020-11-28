"""Setup script for python-telegram-bot-api"""
from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    required_packages = f.read().splitlines()

with open(path.join(here, 'VERSION')) as f:
    version = f.read().strip()

setup(
    name="python-telegram-bot-api",
    version=version,
    author="Dmitriy Kalekin",
    author_email="herrhorror@gmail.com",
    description="Simple and fast client to call rest-api endpoints `api.telegram.org` using `aiohttp` package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DmitriyKalekin/python-telegram-bot-api",
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    keywords='pydantic telegram api bot',
    classifiers=[
        # "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Operating System :: OS Independent",
    ],
    install_requires=required_packages,
    python_requires='>=3.7, <4',
    project_urls={
        "Source": "https://github.com/DmitriyKalekin/python-telegram-bot-api",
    },
)
