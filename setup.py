"""Setup script for telegram-bot-api"""
import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

requirements = ["aiohttp>=3.6.2"]

setuptools.setup(
	name="python-telegram-bot-api",
	version="0.0.1",
	author="Dmitriy Kalekin",
	author_email="herrhorror@gmail.com",
	description="Simple and fast client to call rest-api endpoints `api.telegram.org` using `aiohttp` package.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/DmitriyKalekin/python-telegram-bot-api",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3.8",
		"License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
		"Operating System :: OS Independent",
	],
	install_requires=[
		"aiohttp"
	],
	python_requires='>=3.7',
)
