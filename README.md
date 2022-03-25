<h1 align="center">Sublib</h1>

<p align="center">Python library for easier management and processing of subtitle files.</p>

<p  align="center">
	<a style="text-decoration:none" href="https://github.com/TheFifthLeaf/sublib/releases">
		<img src="https://img.shields.io/github/v/release/TheFifthLeaf/sublib?color=3C7DD9" alt="Releases">
	</a>
	<a style="text-decoration:none" href="https://www.python.org/downloads/">
		<img src="https://img.shields.io/badge/python-3.6%2B-3C7DD9" alt="Python Version">
	</a>
	<a style="text-decoration:none" href="https://choosealicense.com/licenses/gpl-3.0/">
		<img src="https://img.shields.io/badge/license-GPL%20V3-3C7DD9" alt="License GPLv3">
	</a>
	<a href="https://www.codefactor.io/repository/github/thefifthleaf/sublib">
		<img src="https://img.shields.io/codefactor/grade/github/TheFifthLeaf/sublib/main?color=3C7DD9" alt="CodeFactor" />
	</a>
</p>

## Installation

Currently, Sublib supports releases of Python 3.6 onwards. To install the current release:
```bash
python -m pip install sublib
```
..or you can just download package files via [GitHub](https://github.com/TheFifthLeaf/sublib/archive/refs/tags/v1.2.0.zip).

## Testing

### Execute tests
Checks can be run via:
```bash
python -m pytest tests
```

### Tests coverage
You can check coverage by yourself:
```bash
python -m coverage report -m
```
Summary:
| Name 		              | Stmts | Miss | Cover |
|:------------------------|------:|-----:|------:|
| sublib\\\_\_init\_\_.py | 2     | 0    | 100%  |
| sublib\sublib.py        | 144   | 0    | 100%  |

## Getting Started

To use the module you need to import it first:
```python
import sublib
```

Detection of the subtitle format:
```python
# If the format is unknown it will return 'undefined'
sub_format = sublib.detect("subtitle.srt", "utf-8")
```

Creation of the subtitle object:
```python
# You can choose from: MPlayer2, SubRip, MicroDVD, TMPlayer
subtitle = sublib.SubRip("subtitle.srt", "utf-8")
```

Each subtitle object has two methods:
```python
# Returns a list of lines in a universal format
# [[datetime.timedelta(...), datetime.timedelta(...), 'Line 01|Line 02], ...]
general = subtitle.get_general_format()
```
```python
# Formats lines and adds them to an existing object
empty_subtitle = sublib.MPlayer2()
empty_subtitle.set_from_general_format(general)
```

..and several attributes:
```python
subtitle.path		# The file path you used to create the object
subtitle.encoding 	# The encoding you used to create the object
subtitle.content 	# The contents of the file as a list of lines
subtitle.pattern 	# The regex format of a specific type of subtitle
```

Boolean conversion:
```python
# Empty object will return False
print(bool(subtitle))
# Object with content will return True
subtitle.set_from_general_format(general)
if subtitle:
	print(subtitle.content)
```

Object content comparison:
```python
# The contents of the 'content' attributes of each object are compared
if subtitle_1 != subtitle_2:
	subtitle_2.content = subtitle_1.content
```

Return the number of lines in the file:
```python
# In all formats except SubRip, this is the number of lines that will be displayed
print(len(subtitle))
```

Presence of a string in the subtitles may be check with 'in' statement:
```python
# The individual lines are searched sequentially
if "some text" in subtitle:
	return "Yes"
```

Iterating over the subtitle lines:
```python
# The individual lines are searched sequentially
for line in subtitle:
	print(line)
```

## Supported formats

- as **mpl** - MPlayer2 (.txt)
- as **srt** - SubRip (.srt)
- as **sub** - MicroDVD (.sub)
- as **tmp** - TMPlayer (.txt)

## Contributing

Pull requests are welcome.

## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)