import builtins
import datetime

import pytest
import pytest_mock
import sublib


class TestSubRipClass:

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
            'Line 05'
        ]
    ]

    def test_subrip_get_general_format(self, mocker):
        test_data = "1\n"\
                    "00:01:00,060 --> 00:01:03,105\n"\
                    "Line 01\n"\
                    "Line 02\n\n"\
                    "2\n00:01:03,272 --> 00:01:05,440\n"\
                    "Line 03\n"\
                    "Line 04\n\n"\
                    "3\n"\
                    "00:01:05,607 --> 00:01:06,775\n"\
                    "Line 05\n\n"
        mocker.patch(
            "builtins.open",
            mocker.mock_open(read_data=test_data)
        )
        subtitle = sublib.SubRip("file.txt", "utf-8")
        assert self.general_lines == subtitle.get_general_format()

    def test_subrip_set_from_general_format(self):
        test_data = [
            "1\n"
            "00:01:00,060 --> 00:01:03,105\n"
            "Line 01\n"
            "Line 02\n\n",
            "2\n"
            "00:01:03,272 --> 00:01:05,440\n"
            "Line 03\n"
            "Line 04\n\n",
            "3\n"
            "00:01:05,607 --> 00:01:06,775\n"
            "Line 05\n\n"
        ]
        subtitle = sublib.SubRip()
        subtitle.set_from_general_format(self.general_lines)
        assert test_data == subtitle.content
