import re
import sys
import datetime as dt


# Detect Function


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


# MPL Functions


def from_mpl(file):
    """Convert MPlayer2 formatted lines to general list
    Parameters:
        file (file): The open file from which the lines will be read
    Returns:
        list: lines one by one in general format
    """
    lines = [line.split("]", 2) for line in (line.rstrip("\n") for line in file)]
    for line in lines:
        line[0] = dt.timedelta(
            seconds=round(float(line[0].replace("[", "")) / 10.0, 1)    # MPL use as time: sec * 10
        )
        line[1] = dt.timedelta(
            seconds=round(float(line[1].replace("[", "")) / 10.0, 1)
        )
        line[2] = line[2].lstrip()
    return lines


def to_mpl(lines):
    """Convert general list to MPlayer2 foramt
    Parameters:
        lines (list): Lines in general formatt that will be converted
    Returns:
        list: lines one by one in MPlayer2 format
    """
    for line in lines:
        line[0] = round(line[0].total_seconds() * 10)   # MPL use as time: sec * 10
        line[1] = round(line[1].total_seconds() * 10)
    return [f"[{line[0]}][{line[1]}] {line[2]}" for line in lines]


# SRT Functions


def from_srt(file):
    """Convert SubRip formatted lines to general list
    Parameters:
        file (file): The open file from which the lines will be read
    Returns:
        list: lines one by one in general format
    """
    lines, temp = [], []
    for line in file:
        if line != "\n":
            temp.append(line.rstrip("\n"))
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


def to_srt(lines):
    """Convert general list to SubRip foramt
    Parameters:
        lines (list): Lines in general formatt that will be converted
    Returns:
        list: lines one by one in SubRip format
    """
    for line in lines:
        line[0] = str(line[0])
        line[1] = str(line[1])
        if len(line[0]) == 7:
            line[0] = line[0] + "." + "".zfill(6)   # If no microsecons, fill with zeros
        if len(line[1]) == 7:
            line[1] = line[1] + "." + "".zfill(6)
        line[0] = dt.datetime.strptime(line[0], "%H:%M:%S.%f")
        line[1] = dt.datetime.strptime(line[1], "%H:%M:%S.%f")
        line[0] = line[0].strftime("%H:%M:%S.%f").replace(".", ",")
        line[1] = line[1].strftime("%H:%M:%S.%f").replace(".", ",")
        line[0] = line[0][:len(line[0]) - 3]
        line[1] = line[1][:len(line[1]) - 3]
        line[2] = line[2].replace("|", "\n")
    return [f"{num}\n{line[0]} --> {line[1]}\n{line[2]}\n"
            for num, line in enumerate(lines, 1)]


# SUB Functions


def from_sub(file):
    """Convert MicroDVD formatted lines to general list
    Parameters:
        file (file): The open file from which the lines will be read
    Returns:
        list: lines one by one in general format
    """
    lines = [line.split("}", 2) for line in (line.rstrip("\n") for line in file)]
    for line in lines:
        line[0] = dt.timedelta(
            seconds=round(float(line[0].replace("{", "")) / 23.976, 3)  # SUB use frames as time
        )
        line[1] = dt.timedelta(
            seconds=round(float(line[1].replace("{", "")) / 23.976, 3)
        )
        for style in re.findall(r"{.*}", line[2]):
            line[2] = line[2].replace(style, "")
    return lines


def to_sub(lines):
    """Convert general list to MicroDVD foramt
    Parameters:
        lines (list): Lines in general formatt that will be converted
    Returns:
        list: lines one by one in MicroDVD format
    """
    for line in lines:
        line[0] = round(line[0].total_seconds() * 23.976)   # SUB use frames as time
        line[1] = round(line[1].total_seconds() * 23.976)
    return [f"{{{line[0]}}}{{{line[1]}}}{line[2]}" for line in lines]


# TMP Functions


def from_tmp(file):
    """Convert TMPlayer formatted lines to general list
    Parameters:
        file (file): The open file from which the lines will be read
    Returns:
        list: lines one by one in general format
    """
    lines = [line.split(":", 3) for line in (line.rstrip("\n") for line in file)]
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


def to_tmp(lines):
    """Convert general list to TMPlayer foramt
    Parameters:
        lines (list): Lines in general formatt that will be converted
    Returns:
        list: lines one by one in TMPlayer format
    """
    for line in lines:
        line[0] = str(line[0])
        if len(line[0]) == 7:
            line[0] = line[0] + "." + "".zfill(6)   # If no microsecons, fill with zeros
        line[0] = dt.datetime.strptime(line[0], "%H:%M:%S.%f")
        line[0] = line[0].strftime("%H:%M:%S.%f")
        line[0] = line[0][:len(line[0]) - 7]
    return [f"{line[0]}:{line[2]}" for line in lines]


# Subtitle class


class Subtitle:

    def __init__(self, path=None, encoding=None):
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
        return f'{self.__class__.__name__}("{self.path}", "{self.encoding}")'

    def __repr__(self):
        return f'{self.__class__.__name__}(path="{self.path}", encoding="{self.encoding}")'

    def __bool__(self):
        return False if self.content is None else True

    def __eq__(self, other):
        return True if self.content == other.content else False

    def __len__(self):
        return len(self.content)

    def __contains__(self, item):
        for line in self.content:
            if line.count(item) > 0:
                return True

    def __iter__(self):
        self._i = 0
        return self

    def __next__(self):
        line = self.content[self._i]
        self._i += 1
        return line


class MPlayer2(Subtitle):

    def __init__(self, path=None, encoding=None):
        super().__init__(path, encoding)
        self.format = r"\\[[0-9]+\\]\\[[0-9]+\\] .*\n"

    def get_general_format(self):
        lines = [line.split("]", 2) for line in (line.rstrip("\n") for line in self.content)]
        for line in lines:
            line[0] = dt.timedelta(
                seconds=round(float(line[0].replace("[", "")) / 10.0, 1)
            )
            line[1] = dt.timedelta(
                seconds=round(float(line[1].replace("[", "")) / 10.0, 1)
            )
            line[2] = line[2].lstrip()
        return lines

    def set_from_general_format(self, lines):
        for line in lines:
            line[0] = round(line[0].total_seconds() * 10)
            line[1] = round(line[1].total_seconds() * 10)
        self.content = [f"[{line[0]}][{line[1]}] {line[2]}" for line in lines]


class SubRip(Subtitle):

    def __init__(self, path=None, encoding=None):
        super().__init__(path, encoding)
        self.format = r"[0-9]+\n[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3} --> [0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}\n*\n"

    def get_general_format(self):
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
        for line in lines:
            line[0] = str(line[0])
            line[1] = str(line[1])
            if len(line[0]) == 7:
                line[0] = line[0] + "." + "".zfill(6)
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

    def __init__(self, path=None, encoding=None):
        super().__init__(path, encoding)
        self.format = r"{[0-9]+}{[0-9]+}.*\n"

    def get_general_format(self):
        lines = [line.split("}", 2) for line in (line.rstrip("\n") for line in self.content)]
        for line in lines:
            line[0] = dt.timedelta(
                seconds=round(float(line[0].replace("{", "")) / 23.976, 3)
            )
            line[1] = dt.timedelta(
                seconds=round(float(line[1].replace("{", "")) / 23.976, 3)
            )
            for style in re.findall(r"{.*}", line[2]):
                line[2] = line[2].replace(style, "")
        return lines

    def set_from_general_format(self, lines):
        for line in lines:
            line[0] = round(line[0].total_seconds() * 23.976)
            line[1] = round(line[1].total_seconds() * 23.976)
        self.content = [f"{{{line[0]}}}{{{line[1]}}}{line[2]}" for line in lines]


class TMPlayer(Subtitle):

    def __init__(self, path=None, encoding=None):
        super().__init__(path, encoding)
        self.format = r"[0-9]+:[0-9]+:[0-9]+:.*\n"

    def get_general_format(self):
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
        for line in lines:
            line[0] = str(line[0])
            if len(line[0]) == 7:
                line[0] = line[0] + "." + "".zfill(6)   # If no microsecons, fill with zeros
            line[0] = dt.datetime.strptime(line[0], "%H:%M:%S.%f")
            line[0] = line[0].strftime("%H:%M:%S.%f")
            line[0] = line[0][:len(line[0]) - 7]
        self.content = [f"{line[0]}:{line[2]}" for line in lines]
