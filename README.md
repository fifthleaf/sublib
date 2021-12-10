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

Currently, sublib supports releases of Python 3.6 onwards. To install the current release:
```bash
pip install --upgrade sublib
```

## Getting Started

You have a few function at your disposal.

#### detect(file_name, file_encoding)
```python
from sublib import detect

# This will detect subrip format
file_format = detect("subtitle.srt", "utf-8")
```

#### from_mpl(opened_file), to_mpl(general_lines)
```python
from sublib import from_mpl, to_mpl

# This will read MPlayer2 file and convert to general list
with open("subtitle.txt", "rt", encoding="utf-8") as file:
	general_list = from_mpl(file)

# This will read lines from general list and convert to MPlayer2 format
formated_lines = to_mpl(general_list)
```

#### from_srt(opened_file), to_srt(general_lines)
```python
from sublib import from_srt, to_srt

# This will read SubRip file and convert to general list
with open("subtitle.srt", "rt", encoding="utf-8") as file:
	general_list = from_srt(file)

# This will read lines from general list and convert to SubRip format
formated_lines = to_srt(general_list)
```

#### from_sub(opened_file), to_sub(general_lines)
```python
from sublib import from_sub, to_sub

# This will read MicroDVD file and convert to general list
with open("subtitle.sub", "rt", encoding="utf-8") as file:
	general_list = from_sub(file)

# This will read lines from general list and convert to MicroDVD format
formated_lines = to_sub(general_list)
```

#### from_tmp(opened_file), to_tmp(general_lines)
```python
from sublib import from_tmp, to_tmp

# This will read TMPlayer file and convert to general list
with open("subtitle.txt", "rt", encoding="utf-8") as file:
	general_list = from_tmp(file)

# This will read lines from general list and convert to TMPlayer format
formated_lines = to_tmp(general_list)
```


## Supported formats

- as **srt** - SubRip (.srt)
- as **sub** - MicroDVD (.sub)
- as **mpl** - MPlayer2 (.txt)
- as **tmp** - TMPlayer (.txt)

## Contributing

Pull requests are welcome.

## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)