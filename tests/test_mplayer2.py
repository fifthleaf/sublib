import builtins
import datetime

import pytest
import pytest_mock
import sublib


class TestMPlayer2Class:

    general_lines = [
        [
            datetime.timedelta(seconds=60, microseconds=100000),
            datetime.timedelta(seconds=63, microseconds=100000),
            'Line 01|Line 02'
        ],
        [
            datetime.timedelta(seconds=63, microseconds=300000),
            datetime.timedelta(seconds=65, microseconds=400000),
            'Line 03|Line 04'
        ],
        [
            datetime.timedelta(seconds=65, microseconds=600000),
            datetime.timedelta(seconds=66, microseconds=800000),
            'Line 04'
        ]
    ]

    def test_mplayer2_get_general_format(self, mocker):
        test_data = "[601][631] Line 01|Line 02\n"\
                    "[633][654] Line 03|Line 04\n"\
                    "[656][668] Line 04\n"
        mocker.patch(
            "builtins.open",
            mocker.mock_open(read_data=test_data)
        )
        subtitle = sublib.MPlayer2("file.txt", "utf-8")
        assert self.general_lines == subtitle.get_general_format()

    def test_mplayer2_set_from_general_format(self):
        test_data = [
            "[601][631] Line 01|Line 02",
            "[633][654] Line 03|Line 04",
            "[656][668] Line 04"
        ]
        subtitle = sublib.MPlayer2()
        subtitle.set_from_general_format(self.general_lines)
        assert test_data == subtitle.content
