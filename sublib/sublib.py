import re
import sys
import datetime


# Functions


def detect(path: str, encoding: str) -> str:
    """
    Specifies the subtitle format.

    Parameters
    ----------
    path: str
        Path to a textual subtitle file.
    encoding: str
        Representation of encoding type.

    Returns
    ----------
    str
        Detected format.
    """
    with open(path, "rt", encoding=encoding, errors="ignore") as f:
        content = f.read()
    regex_mpl = "\\[[0-9]+\\]\\[[0-9]+\\] .*\n"
    regex_srt = "[0-9]+\n[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3} "\
                "--> [0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}\n.*\n\n"
    regex_sub = "{[0-9]+}{[0-9]+}.*\n"
    regex_tmp = "[0-9]+:[0-9]+:[0-9]+:.*\n"
    if re.findall(regex_mpl, content):
        return "mpl"
    elif re.findall(regex_srt, content):
        return "srt"
    elif re.findall(regex_sub, content):
        return "sub"
    elif re.findall(regex_tmp, content):
        return "tmp"
    else:
        return "undefined"


# Classes


class Subtitle:
    """
    Represent subtitle file in general.
    Specific format classes inherit from it.

    Attributes
    ----------
    path: str
        Path to a textual subtitle file.
    encoding: str
        Representation of encoding type.
    content: list
        Lines of the subtitle file.
    _iterator: int
        Iter number when iterator set.

    Methods
    ----------
    __init__(path, encoding)
        Create class instance.
    __str__()
        Subtitle("arg1", "arg2")
    __repr__()
        Subtitle(path="arg1", encoding="arg2")
    __bool__()
        Whether contains lines.
    __eq__(other)
        Whether both contents are equal.
    __len__()
        Count of content lines.
    __contains__(item)
        Whether item in any line.
    __iter__()
        Behave as iterator.
    __next__()
        Give a next line.
    """

    def __init__(self, path: str = "", encoding: str = "") -> None:
        """
        Construct a class instance.

        Parameters
        ----------
        path: str
            Path to a textual subtitle file.
        encoding: str
            Representation of encoding type.

        Returns
        ----------
        None
        """
        self.path = path
        self.encoding = encoding
        if self.path != "" and self.encoding != "":
            try:
                with open(path, "rt", encoding=encoding, errors="ignore") as f:
                    self.content = [
                        line.rstrip("\n")
                        if line != "\n" else line
                        for line in f.readlines()
                    ]
            except Exception:
                self.content = []
                print(sys.exc_info())
        else:
            self.content = []

    def __str__(self) -> str:
        """
        Specifies how str() is displayed.

        Parameters
        ----------
        None

        Returns
        ----------
        str
            class_name("path", "encoding")
        """
        return f'{self.__class__.__name__}'\
               f'("{self.path}", "{self.encoding}")'

    def __repr__(self) -> str:
        """
        Specifies how repr() is displayed.

        Parameters
        ----------
        None

        Returns
        ----------
        str
            class_name(path="path", encoding="encoding")
        """
        return f'{self.__class__.__name__}'\
               f'(path="{self.path}", encoding="{self.encoding}")'

    def __bool__(self) -> bool:
        """
        Specifies what logic check should return.

        Parameters
        ----------
        None

        Returns
        ----------
        bool
            Whether self.content is empty.
        """
        return bool(self.content)

    def __eq__(self, other: "Subtitle") -> bool:
        """
        Specifies whether subtitle objects are equal.

        Parameters
        ----------
        other: Subtitle
            Object to compare.

        Returns
        ----------
        bool
            Whether the contents of both are equal.
        """
        return self.content == other.content

    def __len__(self) -> int:
        """
        Specifies what len() return.

        Parameters
        ----------
        None

        Returns
        ----------
        int
            Number of lines in file.
        """
        return len(self.content)

    def __contains__(self, item: str) -> bool:
        """
        Specifies "in" behavior:
        Search for match in every line.

        Parameters
        ----------
        item: str
            The string to be searched for.

        Returns
        ----------
        bool
            Whether the string is found.
        """
        for line in self.content:
            if item in line:
                return True
            else:
                return False

    def __iter__(self) -> "Subtitle":
        """
        Specifies preparations for
        being an iterator.

        Parameters
        ----------
        None

        Returns
        ----------
        Subtitle
            Iterator of itself.
        """
        self._iterator = 0
        return self

    def __next__(self) -> str:
        """
        Specifies the behavior of
        an object as an iterator.

        Parameters
        ----------
        None

        Returns
        ----------
        str
            Specified line.
        """
        line = self.content[self._iterator]
        self._iterator += 1
        return line


class MPlayer2(Subtitle):
    """
    Represent MPlayer2 subtitle format.

    Attributes
    ----------
    path: str
        Path to a textual subtitle file.
    encoding: str
        Representation of encoding type.
    content: list
        Lines of the subtitle file.
    pattern: str
        RegEx pattern of MPlayer2 format.
    _iterator: int
        Iter number when iterator set.

    Methods
    ----------
    get_general_format()
        Return content in general format.
    set_from_general_format(lines)
        Set lines to MPlayer2 format.
    __init__(path, encoding)
        Create class instance.
    __str__()
        MPlayer2("arg1", "arg2")
    __repr__()
        MPlayer2(path="arg1", encoding="arg2")
    __bool__()
        Whether contains lines.
    __eq__(other)
        Whether both contents are equal.
    __len__()
        Count of content lines.
    __contains__(item)
        Whether item in any line.
    __iter__()
        Behave as iterator.
    __next__()
        Give a next line.
    """

    pattern = r"\\[[0-9]+\\]\\[[0-9]+\\] .*\n"

    def get_general_format(self) -> list:
        """
        Get object content and return
        converted to general format.

        Parameters
        ----------
        None

        Returns
        ----------
        list
            Lines in general format.
        """
        lines = [line.rstrip("\n") for line in self.content]
        lines = [line.split("]", 2) for line in lines]
        for line in lines:
            seconds = float(line[0].replace("[", "")) / 10.0
            line[0] = datetime.timedelta(seconds=round(seconds, 1))
            seconds = float(line[1].replace("[", "")) / 10.0
            line[1] = datetime.timedelta(seconds=round(seconds, 1))
            line[2] = line[2].lstrip()
        return lines

    def set_from_general_format(self, lines: list) -> None:
        """
        Convert given lines to specified
        format and set as object content.

        Parameters
        ----------
        lines: list
            Lines in general format.

        Returns
        ----------
        None
        """
        for line in lines:
            line[0] = round(line[0].total_seconds() * 10)
            line[1] = round(line[1].total_seconds() * 10)
        self.content = [
            f"[{line[0]}][{line[1]}] {line[2]}"
            for line in lines
        ]


class SubRip(Subtitle):
    """
    Represent SubRip subtitle format.

    Attributes
    ----------
    path: str
        Path to a textual subtitle file.
    encoding: str
        Representation of encoding type.
    content: list
        Lines of the subtitle file.
    pattern: str
        RegEx pattern of SubRip format.
    _iterator: int
        Iter number when iterator set.

    Methods
    ----------
    get_general_format()
        Return content in general format.
    set_from_general_format(lines)
        Set lines to SubRip format.
    __init__(path, encoding)
        Create class instance.
    __str__()
        SubRip("arg1", "arg2")
    __repr__()
        SubRip(path="arg1", encoding="arg2")
    __bool__()
        Whether contains lines.
    __eq__(other)
        Whether both contents are equal.
    __len__()
        Count of content lines.
    __contains__(item)
        Whether item in any line.
    __iter__()
        Behave as iterator.
    __next__()
        Give a next line.
    """

    pattern = r"[0-9]+\n[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3} "\
              r"--> [0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}\n*\n"

    def get_general_format(self) -> list:
        """
        Get object content and return
        converted to general format.

        Parameters
        ----------
        None

        Returns
        ----------
        list
            Lines in general format.
        """
        lines, temp = [], []
        for line in self.content:
            if line != "\n":
                temp.append(line)
            else:
                lines.append(temp)
                temp = []
        lines = [
            [*line[1].split(" --> "), "|".join(line[2:])]
            for line in lines
        ]
        for line in lines:
            line[0] = datetime.datetime.strptime(line[0], "%H:%M:%S,%f")
            line[1] = datetime.datetime.strptime(line[1], "%H:%M:%S,%f")
            for n in range(2):
                line[n] = datetime.timedelta(
                    hours=line[n].hour,
                    minutes=line[n].minute,
                    seconds=line[n].second,
                    microseconds=line[n].microsecond
                )
            for style in re.findall(r"</.*>", line[2]):
                line[2] = line[2].replace(style, "")
            for style in re.findall(r"<.*>", line[2]):
                line[2] = line[2].replace(style, "")
        return lines

    def set_from_general_format(self, lines: list) -> None:
        """
        Convert given lines to specified
        format and set as object content.

        Parameters
        ----------
        lines: list
            Lines in general format.

        Returns
        ----------
        None
        """
        for line in lines:
            line[0] = str(line[0])
            line[1] = str(line[1])
            if len(line[0]) == 7:
                line[0] = line[0] + "." + "".zfill(6)
            if len(line[1]) == 7:
                line[1] = line[1] + "." + "".zfill(6)
            line[0] = datetime.datetime.strptime(line[0], "%H:%M:%S.%f")
            line[1] = datetime.datetime.strptime(line[1], "%H:%M:%S.%f")
            line[0] = line[0].strftime("%H:%M:%S.%f").replace(".", ",")
            line[1] = line[1].strftime("%H:%M:%S.%f").replace(".", ",")
            line[0] = line[0][:len(line[0]) - 3]
            line[1] = line[1][:len(line[1]) - 3]
            line[2] = line[2].replace("|", "\n")
        self.content = [
            f"{num}\n{line[0]} --> {line[1]}\n{line[2]}\n\n"
            for num, line in enumerate(lines, 1)
        ]


class MicroDVD(Subtitle):
    """
    Represent MicroDVD subtitle format.

    Attributes
    ----------
    path: str
        Path to a textual subtitle file.
    encoding: str
        Representation of encoding type.
    content: list
        Lines of the subtitle file.
    pattern: str
        RegEx pattern of MicroDVD format.
    _iterator: int
        Iter number when iterator set.

    Methods
    ----------
    get_general_format()
        Return content in general format.
    set_from_general_format(lines)
        Set lines to MicroDVD format.
    __init__(path, encoding)
        Create class instance.
    __str__()
        MicroDVD("arg1", "arg2")
    __repr__()
        MicroDVD(path="arg1", encoding="arg2")
    __bool__()
        Whether contains lines.
    __eq__(other)
        Whether both contents are equal.
    __len__()
        Count of content lines.
    __contains__(item)
        Whether item in any line.
    __iter__()
        Behave as iterator.
    __next__()
        Give a next line.
    """

    pattern = r"{[0-9]+}{[0-9]+}.*\n"

    def get_general_format(self) -> list:
        """
        Get object content and return
        converted to general format.

        Parameters
        ----------
        None

        Returns
        ----------
        list
            Lines in general format.
        """
        lines = [line.rstrip("\n") for line in self.content]
        lines = [line.split("}", 2) for line in lines]
        for line in lines:
            seconds = float(line[0].replace("{", "")) / 23.976
            line[0] = datetime.timedelta(seconds=round(seconds, 3))
            seconds = float(line[1].replace("{", "")) / 23.976
            line[1] = datetime.timedelta(seconds=round(seconds, 3))
            for style in re.findall(r"{.*}", line[2]):
                line[2] = line[2].replace(style, "")
        return lines

    def set_from_general_format(self, lines: list) -> None:
        """
        Convert given lines to specified
        format and set as object content.

        Parameters
        ----------
        lines: list
            Lines in general format.

        Returns
        ----------
        None
        """
        for line in lines:
            line[0] = round(line[0].total_seconds() * 23.976)
            line[1] = round(line[1].total_seconds() * 23.976)
        self.content = [
            f"{{{line[0]}}}{{{line[1]}}}{line[2]}"
            for line in lines
        ]


class TMPlayer(Subtitle):
    """
    Represent TMPlayer subtitle format.

    Attributes
    ----------
    path: str
        Path to a textual subtitle file.
    encoding: str
        Representation of encoding type.
    content: list
        Lines of the subtitle file.
    pattern: str
        RegEx pattern of TMPlayer format.
    _iterator: int
        Iter number when iterator set.

    Methods
    ----------
    get_general_format()
        Return content in general format.
    set_from_general_format(lines)
        Set lines to TMPlayer format.
    __init__(path, encoding)
        Create class instance.
    __str__()
        TMPlayer("arg1", "arg2")
    __repr__()
        TMPlayer(path="arg1", encoding="arg2")
    __bool__()
        Whether contains lines.
    __eq__(other)
        Whether both contents are equal.
    __len__()
        Count of content lines.
    __contains__(item)
        Whether item in any line.
    __iter__()
        Behave as iterator.
    __next__()
        Give a next line.
    """

    pattern = r"[0-9]+:[0-9]+:[0-9]+:.*\n"

    def get_general_format(self) -> list:
        """
        Get object content and return
        converted to general format.

        Parameters
        ----------
        None

        Returns
        ----------
        list
            Lines in general format.
        """
        lines = [line.rstrip("\n") for line in self.content]
        lines = [line.split(":", 3) for line in lines]
        lines = [
            [f"{line[0]}:{line[1]}:{line[2]}", line[3]]
            for line in lines
        ]
        for line in lines:
            line[0] = datetime.datetime.strptime(line[0], "%H:%M:%S")
            line[0] = datetime.timedelta(
                hours=line[0].hour,
                minutes=line[0].minute,
                seconds=line[0].second,
                microseconds=line[0].microsecond
            )
            line.insert(1, line[0] + datetime.timedelta(seconds=1))
        return lines

    def set_from_general_format(self, lines: list) -> None:
        """
        Convert given lines to specified
        format and set as object content.

        Parameters
        ----------
        lines: list
            Lines in general format.

        Returns
        ----------
        None
        """
        for line in lines:
            line[0] = str(line[0])
            if len(line[0]) == 7:
                line[0] = line[0] + "." + "".zfill(6)
            line[0] = datetime.datetime.strptime(line[0], "%H:%M:%S.%f")
            line[0] = line[0].strftime("%H:%M:%S.%f")
            line[0] = line[0][:len(line[0]) - 7]
        self.content = [
            f"{line[0]}:{line[2]}"
            for line in lines
        ]
