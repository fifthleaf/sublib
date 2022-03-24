"""
SubLib
========
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

    Subtitle(__builtin__.object)
    |
    |   Represent subtitle file in general.
    |   Specific format classes inherit from it.
    |
    |   Methods:
    |       __init__(path, encoding)
    |       __str__()
    |       __repr__()
    |       __bool__()
    |       __eq__(other)
    |       __len__()
    |       __contains__(item)
    |       __iter__()
    |       __next__()
    |

    MPlayer2(Subtitle)
    |
    |   Represent MPlayer2 subtitle format.
    |
    |   Attributes:
    |       pattern
    |
    |   Methods:
    |       get_general_format()
    |       set_from_general_format(lines)
    |

    SubRip(Subtitle)
    |
    |   Represent SubRip subtitle format.
    |
    |   Attributes:
    |       pattern
    |
    |   Methods:
    |       get_general_format()
    |       set_from_general_format(lines)
    |

    MicroDVD(Subtitle)
    |
    |   Represent MicroDVD subtitle format.
    |
    |   Attributes:
    |       pattern
    |
    |   Methods:
    |       get_general_format()
    |       set_from_general_format(lines)
    |

    TMPlayer(Subtitle)
    |
    |   Represent TMPlayer subtitle format.
    |
    |   Attributes:
    |       pattern
    |
    |   Methods:
    |       get_general_format()
    |       set_from_general_format(lines)
    |

"""

from sublib.sublib import detect, Subtitle, MPlayer2, SubRip, MicroDVD, TMPlayer

__version__ = "1.2.0"
