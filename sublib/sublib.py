import re
import sys
import datetime


# Functions


def detect(filepath: str, encoding: str) -> str:
    """A function to detect subtitle format
    Parameters:
        filepath (str): path to a file that may contain subtitles
        encoding (str): The type of encoding to use when opening the file
    Returns:
        str: detected format or 'undefined'
    """
    regex_mpl = "\\[[0-9]+\\]\\[[0-9]+\\] .*\n"
    regex_srt = "[0-9]+\n[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3} "\
                "--> [0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}\n.*\n\n"
    regex_sub = "{[0-9]+}{[0-9]+}.*\n"
    regex_tmp = "[0-9]+:[0-9]+:[0-9]+:.*\n"
    with open(filepath, "rt", encoding=encoding, errors="ignore") as f:
        content = f.read()
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
    """A class to represent subtitle file in general. The specific format classes inherit from it.
    Attributes:
        path (str): Absolute or relative path to subtitle file that will be read
        encoding (str): Valid encoding that will be use to open a subtitle file
        content (list): The lines of the subtitle file
    """

    def __init__(self, path: str, encoding: str) -> None:
        """Construct classes attributes.
        Parameters:
            path (str): Absolute or relative path to subtitle file that will be read
            encoding (str): Valid encoding that will be use to open a subtitle file
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
        """Specifies how str() is displayed: class_name("path", "encoding")"""
        return f'{self.__class__.__name__}'\
               f'("{self.path}", "{self.encoding}")'

    def __repr__(self) -> str:
        """Specifies how repr() is displayed: class_name(path="path", encoding="encoding")"""
        return f'{self.__class__.__name__}'\
               f'(path="{self.path}", encoding="{self.encoding}")'

    def __bool__(self) -> bool:
        """Specifies what bool() should return: True if self.content is not None"""
        return bool(self.content)

    def __eq__(self, other: "Subtitle") -> bool:
        """Specifies when subtitle calsses are equal: True if self.content value of both is equal"""
        return self.content == other.content

    def __len__(self) -> int:
        """Specifies what len() should return: Number of lines in file"""
        return len(self.content)

    def __contains__(self, item: str) -> bool:
        """Specifies what "in" should do: Search for match in every line"""
        for line in self.content:
            if item in line:
                return True
            else:
                return False

    def __iter__(self) -> "Subtitle":
        """Specifies what iter() should do: Set line index to 0"""
        self._iterator = 0
        return self

    def __next__(self) -> str:
        """Specifies what next() should return: Line of file at a specific index"""
        line = self.content[self._iterator]
        self._iterator += 1
        return line


class MPlayer2(Subtitle):
    """A class to represent MPlayer2 subtitle file.
    Attributes:
        path (str): Absolute or relative path to subtitle file that will be read
        encoding (str): Valid encoding that will be use to open a subtitle file
        content (list): The lines of the subtitle file
        format (str): RegEx of specified format
    """

    def __init__(self, path: str = "", encoding: str = "") -> None:
        """Construct classes attributes.
        Parameters:
            path (str): Absolute or relative path to subtitle file that will be read
            encoding (str): Valid encoding that will be use to open a subtitle file
        """
        super().__init__(path, encoding)
        self.format = r"\\[[0-9]+\\]\\[[0-9]+\\] .*\n"

    def get_general_format(self) -> list:
        """Convert MPlayer2 formatted lines to general list
        Parameters:
            None
        Returns:
            list: lines one by one in general format
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
        """Convert general list to MPlayer2 foramt
        Parameters:
            lines (list): Lines in general formatt that will be converted
        Action:
            It sets self.content from provided list of lines.
        """
        for line in lines:
            line[0] = round(line[0].total_seconds() * 10)
            line[1] = round(line[1].total_seconds() * 10)
        self.content = [
            f"[{line[0]}][{line[1]}] {line[2]}"
            for line in lines
        ]


class SubRip(Subtitle):
    """A class to represent SubRip subtitle file.
    Attributes:
        path (str): Absolute or relative path to subtitle file that will be read
        encoding (str): Valid encoding that will be use to open a subtitle file
        content (list): The lines of the subtitle file
        format (str): RegEx of specified format
    """

    def __init__(self, path: str = "", encoding: str = "") -> None:
        """Construct classes attributes.
        Parameters:
            path (str): Absolute or relative path to subtitle file that will be read
            encoding (str): Valid encoding that will be use to open a subtitle file
        """
        super().__init__(path, encoding)
        self.format = r"[0-9]+\n[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3} "\
                      r"--> [0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}\n*\n"

    def get_general_format(self) -> list:
        """Convert SubRip formatted lines to general list
        Parameters:
            None
        Returns:
            list: lines one by one in general format
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
        """Convert general list to SubRip foramt
        Parameters:
            lines (list): Lines in general formatt that will be converted
        Action:
            It sets self.content from provided list of lines.
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
    """A class to represent MicroDVD subtitle file.
    Attributes:
        path (str): Absolute or relative path to subtitle file that will be read
        encoding (str): Valid encoding that will be use to open a subtitle file
        content (list): The lines of the subtitle file
        format (str): RegEx of specified format
    """

    def __init__(self, path: str = "", encoding: str = "") -> None:
        """Construct classes attributes.
        Parameters:
            path (str): Absolute or relative path to subtitle file that will be read
            encoding (str): Valid encoding that will be use to open a subtitle file
        """
        super().__init__(path, encoding)
        self.format = r"{[0-9]+}{[0-9]+}.*\n"

    def get_general_format(self) -> list:
        """Convert MicroDVD formatted lines to general list
        Parameters:
            None
        Returns:
            list: lines one by one in general format
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
        """Convert general list to MicroDVD foramt
        Parameters:
            lines (list): Lines in general formatt that will be converted
        Action:
            It sets self.content from provided list of lines.
        """
        for line in lines:
            line[0] = round(line[0].total_seconds() * 23.976)
            line[1] = round(line[1].total_seconds() * 23.976)
        self.content = [
            f"{{{line[0]}}}{{{line[1]}}}{line[2]}"
            for line in lines
        ]


class TMPlayer(Subtitle):
    """A class to represent TMPlayer subtitle file.
    Attributes:
        path (str): Absolute or relative path to subtitle file that will be read
        encoding (str): Valid encoding that will be use to open a subtitle file
        content (list): The lines of the subtitle file
        format (str): RegEx of specified format
    """

    def __init__(self, path: str = "", encoding: str = "") -> None:
        """Construct classes attributes.
        Parameters:
            path (str): Absolute or relative path to subtitle file that will be read
            encoding (str): Valid encoding that will be use to open a subtitle file
        """
        super().__init__(path, encoding)
        self.format = r"[0-9]+:[0-9]+:[0-9]+:.*\n"

    def get_general_format(self) -> list:
        """Convert TMPlayer formatted lines to general list
        Parameters:
            None
        Returns:
            list: lines one by one in general format
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
        """Convert general list to TMPlayer foramt
        Parameters:
            lines (list): Lines in general formatt that will be converted
        Action:
            It sets self.content from provided list of lines.
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
