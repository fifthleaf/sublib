# Sublib

[![Release](https://img.shields.io/github/v/release/TheFifthLeaf/sublib?color=3C7DD9)](https://github.com/TheFifthLeaf/sublib/releases)
[![Min. Python version](https://img.shields.io/badge/python-3.6%2B-3C7DD9)](https://www.python.org/downloads/)
[![License GPLv3](https://img.shields.io/badge/license-GPL%20V3-3C7DD9)](https://choosealicense.com/licenses/gpl-3.0/)
[![Code quality](https://img.shields.io/codefactor/grade/github/TheFifthLeaf/sublib/main?color=3C7DD9)](https://www.codefactor.io/repository/github/thefifthleaf/sublib)
[![Tests](https://github.com/TheFifthLeaf/sublib/actions/workflows/tests.yml/badge.svg)](https://github.com/TheFifthLeaf/sublib/actions/workflows/tests.yml)

Python library for easier management and processing of subtitle files.
Easily manage their content and conveniently use it in your own projects.

Features
- Read files data
- Convert subtitles formats
- Process content separated into lines
- Search for strings in data
- Acquire specific lines
- Detect used format

## Installation
Download the latest version from `PyPi`
```bash
python -m pip install sublib
```
[More](https://github.com/TheFifthLeaf/sublib/blob/main/docs/sublib-1.2.0-doc.md#installation)

## Testing
Perform the tests with `pytest` and `pytest-mock`
```bash
python -m pytest tests
```
[More](https://github.com/TheFifthLeaf/sublib/blob/main/docs/sublib-1.2.0-doc.md#testing)

## Basic usage
First of all, import the `package`
```python
import sublib
```
Each of the [supported](https://github.com/TheFifthLeaf/sublib/blob/main/docs/sublib-1.2.0-doc.md#formats) formats of subtitles is represent by its `class`
```python
# Create a subtitle instance
subtitle = sublib.SubRip("subtitle.srt", "utf-8")
```
All subtitles classes have a few `methods` and `attributes`
```python
# Get object content in a universal format
general = subtitle.get_general_format()

# Set a new object from this format
another_subtitle = sublib.MicroDVD()
another_subtitle.set_from_general_format(general)

# Print subtitle lines
print(another_subtitle.content)
```
[More](https://github.com/TheFifthLeaf/sublib/blob/main/docs/sublib-1.2.0-doc.md#usage)

## Advanced usage
Please, take a look if you need more [details](https://github.com/TheFifthLeaf/sublib/blob/main/docs/sublib-1.2.0-doc.md#details)

## Contributing
Pull requests are welcome!
