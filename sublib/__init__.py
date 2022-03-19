"""Python library for easier management and processing of subtitle files.

Variables:

    __version__: str

Functions:

    detect(path_file: str, encoding: str) -> format: str

Classes:

    Subtitle(path: str, encoding: str)
        get_general_format() -> lines: list
        set_from_general_format(lines: list)

    MPlayer2(path: str, encoding: str)
        get_general_format() -> lines: list
        set_from_general_format(lines: list)

    SubRip(path: str, encoding: str)
        get_general_format() -> lines: list
        set_from_general_format(lines: list)

    MicroDVD(path: str, encoding: str)
        get_general_format() -> lines: list
        set_from_general_format(lines: list)

    TMPlayer(path: str, encoding: str)
        get_general_format() -> lines: list
        set_from_general_format(lines: list)

Descriptions:

    __version__ - A variable that store package version.
    detect      - A function to detect subtitle format.
    Subtitle    - A class to represent subtitle file in general.
    MPlayer2    - A class to represent MPlayer2 subtitle file.
    SubRip      - A class to represent SubRip subtitle file.
    MicroDVD    - A class to represent MicroDVD subtitle file.
    TMPlayer    - A class to represent TMPlayer subtitle file.

"""

from sublib.sublib import detect, Subtitle, MPlayer2, SubRip, MicroDVD, TMPlayer

__version__ = "1.2.0"
