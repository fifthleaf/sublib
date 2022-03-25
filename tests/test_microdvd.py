import builtins
import datetime

import pytest
import pytest_mock
import sublib


class TestMicroDVDClass:

    general_lines = [
        [
            datetime.timedelta(seconds=60, microseconds=60000),
            datetime.timedelta(seconds=63, microseconds=105000),
            'Line 01|Line 02'
        ],
        [
            datetime.timedelta(seconds=63, microseconds=272000),
            datetime.timedelta(seconds=65, microseconds=440000),
            'Line 03|Line 04'
        ],
        [
            datetime.timedelta(seconds=65, microseconds=607000),
            datetime.timedelta(seconds=66, microseconds=775000),
            'Line 04'
        ]
    ]

    def test_microdvd_get_general_format(self, mocker):
        test_data = "{1440}{1513}{b}Line 01|Line 02\n"\
                    "{1517}{1569}Line 03|Line 04\n"\
                    "{1573}{1601}Line 04\n"
        mocker.patch(
            "builtins.open",
            mocker.mock_open(read_data=test_data)
        )
        subtitle = sublib.MicroDVD("file.txt", "utf-8")
        assert self.general_lines == subtitle.get_general_format()

    def test_microdvd_set_from_general_format(self):
        test_data = [
            "{1440}{1513}Line 01|Line 02",
            "{1517}{1569}Line 03|Line 04",
            "{1573}{1601}Line 04"
        ]
        subtitle = sublib.MicroDVD()
        subtitle.set_from_general_format(self.general_lines)
        assert test_data == subtitle.content
