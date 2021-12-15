import re
import sys
import datetime as dt


# Functions


def detect(path_file, encoding):
    """Detect subtitle format
    Parameters:
        path_file (str): path to a file that may contain subtitles
        encoding (str): The type of encoding to use when opening the file
    Returns:
        str: detected format or 'undefined'
    """
    mpl_reg = "\\[[0-9]+\\]\\[[0-9]+\\] .*\n"                                                           # [START][STOP] TEXT\n
    srt_reg = "[0-9]+\n[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3} --> [0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}\n"   # NUM\nSTART --> STOP\n
    sub_reg = "{[0-9]+}{[0-9]+}.*\n"                                                                    # {START}{STOP}TEXT\n
    tmp_reg = "[0-9]+:[0-9]+:[0-9]+:.*\n"                                                               # START:TEXT\n
    with open(path_file, "rt", encoding=encoding, errors="ignore") as file:
        content = file.read()
    if len(re.findall(mpl_reg, content)) > 0:
        result = "mpl"
    elif len(re.findall(sub_reg, content)) > 0:
        result = "sub"
    elif len(re.findall(srt_reg, content)) > 0:
        result = "srt"
    elif len(re.findall(tmp_reg, content)) > 0:
        result = "tmp"
    else:
        result = "undefined"
    return result


# Classes


class Subtitle:
    """A class to represent subtitle file in general. The specific format classes inherit from it.
    Attributes:
        path (str): Absolute or relative path to subtitle file that will be read
        encoding (str): Valid encoding that will be use to open a subtitle file
    """

    def __init__(self, path=None, encoding=None):
        """Construct classes attributes.
        Parameters:
            path (str): Absolute or relative path to subtitle file that will be read
            encoding (str): Valid encoding that will be use to open a subtitle file
        """
        self.path = path
        self.encoding = encoding
        if self.path is not None and \
           self.encoding is not None:
            try:
                with open(path, "rt", encoding=encoding, errors="ignore") as file:
                    self.content = [line.rstrip("\n") if line != "\n" else line
                                    for line in file.readlines()]
            except Exception:
                self.content = None
                print(sys.exc_info())
        else:
            self.content = None

    def __str__(self):
        """Specifies how str() is displayed: class_name("path", "encoding")"""
        return f'{self.__class__.__name__}("{self.path}", "{self.encoding}")'

    def __repr__(self):
        """Specifies how repr() is displayed: class_name(path="path", encoding="encoding")"""
        return f'{self.__class__.__name__}(path="{self.path}", encoding="{self.encoding}")'

    def __bool__(self):
        """Specifies what bool() should return: True if self.content is not None"""
        return False if self.content is None else True

    def __eq__(self, other):
        """Specifies when subtitle calsses are equal: True if self.content value of both is equal"""
        return True if self.content == other.content else False

    def __len__(self):
        """Specifies what len() should return: Number of lines in file"""
        return len(self.content)

    def __contains__(self, item):
        """Specifies what "in" should do: Search for match in every line"""
        for line in self.content:
            if line.count(item) > 0:
                return True

    def __iter__(self):
        """Specifies what iter() should do: Set line index to 0"""
        self._i = 0
        return self

    def __next__(self):
        """Specifies what next() should return: Line of file at a specific index"""
        line = self.content[self._i]
        self._i += 1
        return line


class MPlayer2(Subtitle):
    """A class to represent MPlayer2 subtitle file.
    Attributes:
        path (str): Absolute or relative path to subtitle file that will be read
        encoding (str): Valid encoding that will be use to open a subtitle file
    """

    def __init__(self, path=None, encoding=None):
        """Construct classes attributes.
        Parameters:
            path (str): Absolute or relative path to subtitle file that will be read
            encoding (str): Valid encoding that will be use to open a subtitle file
        """
        super().__init__(path, encoding)
        self.format = r"\\[[0-9]+\\]\\[[0-9]+\\] .*\n"

    def get_general_format(self):
        """Convert MPlayer2 formatted lines to general list
        Parameters:
            None
        Returns:
            list: lines one by one in general format
        """
        lines = [line.split("]", 2) for line in (line.rstrip("\n") for line in self.content)]
        for line in lines:
            line[0] = dt.timedelta(
                seconds=round(float(line[0].replace("[", "")) / 10.0, 1)    # MPL use as time: sec * 10
            )
            line[1] = dt.timedelta(
                seconds=round(float(line[1].replace("[", "")) / 10.0, 1)
            )
            line[2] = line[2].lstrip()
        return lines

    def set_from_general_format(self, lines):
        """Convert general list to MPlayer2 foramt
        Parameters:
            lines (list): Lines in general formatt that will be converted
        Action:
            It sets self.content from provided list of lines.
        """
        for line in lines:
            line[0] = round(line[0].total_seconds() * 10)    # MPL use as time: sec * 10
            line[1] = round(line[1].total_seconds() * 10)
        self.content = [f"[{line[0]}][{line[1]}] {line[2]}" for line in lines]


class SubRip(Subtitle):
    """A class to represent SubRip subtitle file.
    Attributes:
        path (str): Absolute or relative path to subtitle file that will be read
        encoding (str): Valid encoding that will be use to open a subtitle file
    """

    def __init__(self, path=None, encoding=None):
        """Construct classes attributes.
        Parameters:
            path (str): Absolute or relative path to subtitle file that will be read
            encoding (str): Valid encoding that will be use to open a subtitle file
        """
        super().__init__(path, encoding)
        self.format = r"[0-9]+\n[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3} --> [0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}\n*\n"

    def get_general_format(self):
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
        lines = [[*line[1].split(" --> "), "|".join(line[2:])] for line in lines]
        for line in lines:
            line[0] = dt.datetime.strptime(line[0], "%H:%M:%S,%f")
            line[1] = dt.datetime.strptime(line[1], "%H:%M:%S,%f")
            line[0] = dt.timedelta(
                hours=line[0].hour,
                minutes=line[0].minute,
                seconds=line[0].second,
                microseconds=line[0].microsecond
            )
            line[1] = dt.timedelta(
                hours=line[1].hour,
                minutes=line[1].minute,
                seconds=line[1].second,
                microseconds=line[1].microsecond
            )
            for style in re.findall(r"</.*>", line[2]):
                line[2] = line[2].replace(style, "")
            for style in re.findall(r"<.*>", line[2]):
                line[2] = line[2].replace(style, "")
        return lines

    def set_from_general_format(self, lines):
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
                line[0] = line[0] + "." + "".zfill(6)    # If no microsecons, fill with zeros
            if len(line[1]) == 7:
                line[1] = line[1] + "." + "".zfill(6)
            line[0] = dt.datetime.strptime(line[0], "%H:%M:%S.%f")
            line[1] = dt.datetime.strptime(line[1], "%H:%M:%S.%f")
            line[0] = line[0].strftime("%H:%M:%S.%f").replace(".", ",")
            line[1] = line[1].strftime("%H:%M:%S.%f").replace(".", ",")
            line[0] = line[0][:len(line[0]) - 3]
            line[1] = line[1][:len(line[1]) - 3]
            line[2] = line[2].replace("|", "\n")
        self.content = [f"{num}\n{line[0]} --> {line[1]}\n{line[2]}\n"
                        for num, line in enumerate(lines, 1)]


class MicroDVD(Subtitle):
    """A class to represent MicroDVD subtitle file.
    Attributes:
        path (str): Absolute or relative path to subtitle file that will be read
        encoding (str): Valid encoding that will be use to open a subtitle file
    """

    def __init__(self, path=None, encoding=None):
        """Construct classes attributes.
        Parameters:
            path (str): Absolute or relative path to subtitle file that will be read
            encoding (str): Valid encoding that will be use to open a subtitle file
        """
        super().__init__(path, encoding)
        self.format = r"{[0-9]+}{[0-9]+}.*\n"

    def get_general_format(self):
        """Convert MicroDVD formatted lines to general list
        Parameters:
            None
        Returns:
            list: lines one by one in general format
        """
        lines = [line.split("}", 2) for line in (line.rstrip("\n") for line in self.content)]
        for line in lines:
            line[0] = dt.timedelta(
                seconds=round(float(line[0].replace("{", "")) / 23.976, 3)    # SUB use frames as time
            )
            line[1] = dt.timedelta(
                seconds=round(float(line[1].replace("{", "")) / 23.976, 3)
            )
            for style in re.findall(r"{.*}", line[2]):
                line[2] = line[2].replace(style, "")
        return lines

    def set_from_general_format(self, lines):
        """Convert general list to MicroDVD foramt
        Parameters:
            lines (list): Lines in general formatt that will be converted
        Action:
            It sets self.content from provided list of lines.
        """
        for line in lines:
            line[0] = round(line[0].total_seconds() * 23.976)    # SUB use frames as time
            line[1] = round(line[1].total_seconds() * 23.976)
        self.content = [f"{{{line[0]}}}{{{line[1]}}}{line[2]}" for line in lines]


class TMPlayer(Subtitle):
    """A class to represent TMPlayer subtitle file.
    Attributes:
        path (str): Absolute or relative path to subtitle file that will be read
        encoding (str): Valid encoding that will be use to open a subtitle file
    """

    def __init__(self, path=None, encoding=None):
        """Construct classes attributes.
        Parameters:
            path (str): Absolute or relative path to subtitle file that will be read
            encoding (str): Valid encoding that will be use to open a subtitle file
        """
        super().__init__(path, encoding)
        self.format = r"[0-9]+:[0-9]+:[0-9]+:.*\n"

    def get_general_format(self):
        """Convert TMPlayer formatted lines to general list
        Parameters:
            None
        Returns:
            list: lines one by one in general format
        """
        lines = [line.split(":", 3) for line in (line.rstrip("\n") for line in self.content)]
        lines = [[f"{line[0]}:{line[1]}:{line[2]}", f"{line[0]}:{line[1]}:{line[2]}", line[3]]
                 for line in lines]
        for line in lines:
            line[0] = dt.datetime.strptime(line[0], "%H:%M:%S")
            line[1] = dt.datetime.strptime(line[1], "%H:%M:%S")
            line[0] = dt.timedelta(
                hours=line[0].hour,
                minutes=line[0].minute,
                seconds=line[0].second,
                microseconds=line[0].microsecond
            )
            line[1] = dt.timedelta(
                hours=line[1].hour,
                minutes=line[1].minute,
                seconds=line[1].second + 1,
                microseconds=line[1].microsecond
            )
        return lines

    def set_from_general_format(self, lines):
        """Convert general list to TMPlayer foramt
        Parameters:
            lines (list): Lines in general formatt that will be converted
        Action:
            It sets self.content from provided list of lines.
        """
        for line in lines:
            line[0] = str(line[0])
            if len(line[0]) == 7:
                line[0] = line[0] + "." + "".zfill(6)    # If no microsecons, fill with zeros
            line[0] = dt.datetime.strptime(line[0], "%H:%M:%S.%f")
            line[0] = line[0].strftime("%H:%M:%S.%f")
            line[0] = line[0][:len(line[0]) - 7]
        self.content = [f"{line[0]}:{line[2]}" for line in lines]
