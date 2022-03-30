"""
Package for easier management and
processing of subtitle files. Library
allows you to get subtitle data and
convert their formats.

VARIABLES

    __version__
        Contains the package version.

FUNCTONS

    detect(path, encoding)
        Specifies the subtitle format.

CLASSES

    Subtitle(builtins.object)
        Represent subtitle file in general.

    MPlayer2(Subtitle)
        Represent MPlayer2 subtitle format.

    SubRip(Subtitle)
        Represent SubRip subtitle format.

    MicroDVD(Subtitle)
        Represent MicroDVD subtitle format.

    TMPlayer(Subtitle)
        Represent TMPlayer subtitle format.
"""

from sublib.sublib import detect, Subtitle, MPlayer2, SubRip, MicroDVD, TMPlayer

__version__ = "1.2.0"
