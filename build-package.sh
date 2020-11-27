#!/usr/bin/bash

echo  "run script"
rm -rf ./build
rm -rf ./dist
rm -rf ./py3tgbot.egg-info
python3 setup.py sdist bdist_wheel
twine upload --repository testpypi dist/*
twine upload --repository pypi dist/*