#!/usr/bin/bash

echo  "run script"
rm -rf ./build
rm -rf ./dist
rm -rf ./py3tgbot.egg-info
python3 setup.py sdist bdist_wheel
echo "DmitriyKalekin\nNeverstop37!" | twine upload --repository testpypi dist/*
echo "DmitriyKalekin\nNeverstop37!" |twine upload --repository pypi dist/*