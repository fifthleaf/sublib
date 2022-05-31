# Sublib v1.2.1
- [Installation](#installation)
  - [User](#user)
  - [Contributor](#contributor)
- [Testing](#testing)
- [Usage](#usage)
- [Details](#details)
  - [Variables](#variables)
  - [Functions](#functions)
  - [Classes](#classes)
- [Formats](#formats)
- [License](#license)

## Installation
There are two ways to use the library
- As user (PyPi)
- As contributor (archive)

### User
Please download via Pip package
```bash
python -m pip install sublib
```
Now you can use it in your project
```python
import sublib
```

### Contributor
Please download project from GitHub
```bash
# HTTPS
git clone https://github.com/TheFifthLeaf/sublib.git

# SSH
ssh git@github.com:TheFifthLeaf/sublib.git

# GitHub CLI
gh repo clone TheFifthLeaf/sublib
```
Using a virtual environment is usually a good idea
```bash
# Create venv
python -m venv <env_name>

# Activate venv
<env_name>\Scripts\activate
```
Install package, preferably in edit mode
```bash
python -m pip install -e .
```
Install tests dependencies
```bash
python -m pip install -r requirements_dev.txt
```
Now you can develop and test project.

## Testing
Unit tests use the following dependencies
- pytest
- pytest-mock

Run them from project home directory
```bash
# Pytest
python -m pytest tests

# Tox, if installed
python -m tox
```

You can also check tests coverage using Coverage package
```bash
# Create coverage report
# File: .coverage
coverage run --source=sublib -m pytest tests

# Write report in STDOUT
coverage report -m
```

Current coverage:
| Name                    | Stmts | Miss | Cover |
|:------------------------|------:|-----:|------:|
| sublib\\\_\_init\_\_.py | 2     | 0    | 100%  |
| sublib\sublib.py        | 144   | 0    | 100%  |

## Usage

To use the module you need to import it first
```python
import sublib
```

Getting help about package
```python
# To see package content
dir(sublib)

# To see module, function or class help
help(sublib)
help(sublib.detect)
help(sublib.MPlayer2)
```

Detection of the subtitle format
```python
# Supported formats:
# mpl (MPlayer2), srt (SubRip), sub (MicroDVD), tmp (TMPlayer)
# If the format is unknown it will return "undefined"
sub_format = sublib.detect("subtitle.srt", "utf-8")
```

Creation of the subtitle object
```python
# You can choose from:
# MPlayer2, SubRip, MicroDVD, TMPlayer
# (There is also a generic "Subtitle" class)
subtitle = sublib.SubRip("subtitle.srt", "utf-8")
```

Subtitles objects methods
```python
# Applies to all classes except generic "Subtitle"

# Returns a list of lines in a universal (general) format:
# [datetime.timedelta(...), datetime.timedelta(...), 'Line|Line']
subtitle = sublib.SubRip("file.srt", "utf-8")
general = subtitle.get_general_format()

# Format and add lines to specific subtitle object
empty_subtitle = sublib.MPlayer2()
empty_subtitle.set_from_general_format(general)
```

..and several attributes
```python
subtitle.path       # File path you used to create the object
subtitle.encoding   # Encoding you used to create the object
subtitle.content    # Contents of the file as a list of lines
subtitle.pattern    # RegEx format of a specific type of subtitle
```

Boolean conversion
```python
# Empty object will return False
print(bool(subtitle))

# Object with content will return True
subtitle.set_from_general_format(general)
if subtitle:
    print(subtitle.content)
```

Object content comparison
```python
# The contents of the "content"
# attributes of each object are compared
if subtitle_1 != subtitle_2:
    subtitle_2.content = subtitle_1.content
```

Return the number of lines in the file
```python
# In all formats except "SubRip", this is
# the number of lines that will be displayed
print(len(subtitle))
```

Check presence of a string in the subtitles
```python
# The individual lines are searched sequentially
if "some text" in subtitle:
    return "Yes"
```

Iterating over the subtitle lines
```python
# The individual lines are searched sequentially
for line in subtitle:
    print(line)

# Current line number is stored in __line__ variable
iter(subtitle)
print(subtitle.__line__) #0
next(subtitle)
print(subtitle.__line__) #1
```

## Details

### Variables

**\_\_version\_\_ : str** \
&emsp;Contains the package version.

### Functions

**detect(path: str, encoding: str) -> str** \
&emsp;Specifies the subtitle format.

### Classes

**Subtitle(\_\_builtin\_\_.object)** \
&emsp;Represent subtitle file in general. \
&emsp;------------------------------------ \
&emsp;Note \
&emsp;This class is intended to be inherited by specific classes. \
&emsp;Using it directly may have undesirable consequences.

&emsp;**path : str** \
&emsp;&emsp;Path to a textual subtitle file.

&emsp;**encoding : str** \
&emsp;&emsp;Representation of encoding type.

&emsp;**content : list** \
&emsp;&emsp;Lines of the subtitle file.

&emsp;**_iterator : int** \
&emsp;&emsp;Iter number when iterator set.

&emsp;**\_\_init\_\_(self, path: str = "", encoding: str = "") -> None** \
&emsp;&emsp;Construct a class instance.

&emsp;**\_\_str\_\_(self) -> str** \
&emsp;&emsp;Specifies how str() is displayed.

&emsp;**\_\_repr\_\_(self) -> str** \
&emsp;&emsp;Specifies how repr() is displayed.

&emsp;**\_\_bool\_\_(self) -> bool** \
&emsp;&emsp;Specifies what logic check should return.

&emsp;**\_\_eq\_\_(self, other: "Subtitle") -> bool** \
&emsp;&emsp;Specifies whether subtitle objects are equal.

&emsp;**\_\_len\_\_(self) -> int** \
&emsp;&emsp;Specifies what len() return.

&emsp;**\_\_contains\_\_(self, item: str) -> bool** \
&emsp;&emsp;Specifies "in" behavior: Search for match in every line.

&emsp;**\_\_iter\_\_(self) -> "Subtitle"** \
&emsp;&emsp;Specifies preparations for being an iterator.

&emsp;**\_\_next\_\_(self) -> str** \
&emsp;&emsp;Specifies the behavior of an object as an iterator.

**MPlayer2(Subtitle)** \
&emsp;Represent MPlayer2 subtitle format.

&emsp;**pattern : str** \
&emsp;&emsp;RegEx pattern of MPlayer2 format.

&emsp;**get_general_format(self) -> list** \
&emsp;&emsp;Get object content and return converted to general format.

&emsp;**set_from_general_format(self, lines: list) -> None** \
&emsp;&emsp;Convert given lines to specified format and set as object content.

**SubRip(Subtitle)** \
&emsp;Represent SubRip subtitle format.

&emsp;**pattern : str** \
&emsp;&emsp;RegEx pattern of SubRip format.

&emsp;**get_general_format(self) -> list** \
&emsp;&emsp;Get object content and return converted to general format.

&emsp;**set_from_general_format(self, lines: list) -> None** \
&emsp;&emsp;Convert given lines to specified format and set as object content.

**MicroDVD(Subtitle)** \
&emsp;Represent MicroDVD subtitle format.

&emsp;**pattern : str** \
&emsp;&emsp;RegEx pattern of MicroDVD format.

&emsp;**get_general_format(self) -> list** \
&emsp;&emsp;Get object content and return converted to general format.

&emsp;**set_from_general_format(self, lines: list) -> None** \
&emsp;&emsp;Convert given lines to specified format and set as object content.

**TMPlayer(Subtitle)** \
&emsp;Represent TMPlayer subtitle format.

&emsp;**pattern : str** \
&emsp;&emsp;RegEx pattern of TMPlayer format.

&emsp;**get_general_format(self) -> list** \
&emsp;&emsp;Get object content and return converted to general format.

&emsp;**set_from_general_format(self, lines: list) -> None** \
&emsp;&emsp;Convert given lines to specified format and set as object content.

## Formats

Supported:
| Full name | Short name | Default ext. |
|:---------:|:----------:|:------------:|
| MPlayer2  | mpl        | .txt         |
| SubRip    | srt        | .srt         |
| MicroDVD  | sub        | .sub         |
| TMPlayer  | tmp        | .txt         |

## License

The library is distributed under the terms of the [GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/).

Main terms of use:
| Permissions    | Conditions       | Limitations |
|:--------------:|:----------------:|:-----------:|
| Commercial use | Disclose source  | Liability   |
| Distribution   | Copyright notice | Warranty    |
| Modification   | Same license     |             |
| Patent use     | State changes    |             |
| Private use    |                  |             |
