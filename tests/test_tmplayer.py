import builtins
import datetime

import pytest
import pytest_mock
import sublib


class TestTMPlayerClass:

    general_lines = [
        [
            datetime.timedelta(seconds=60),
            datetime.timedelta(seconds=61),
            'Line 01|Line 02'
        ],
        [
            datetime.timedelta(seconds=63),
            datetime.timedelta(seconds=64),
            'Line 03|Line 04'
        ],
        [
            datetime.timedelta(seconds=65),
            datetime.timedelta(seconds=66),
            'Line 04'
        ]
    ]

    def test_tmplayer_get_general_format(self, mocker):
        test_data = "00:01:00:Line 01|Line 02\n"\
                    "00:01:03:Line 03|Line 04\n"\
                    "00:01:05:Line 04\n"
        mocker.patch(
            "builtins.open",
            mocker.mock_open(read_data=test_data)
        )
        subtitle = sublib.TMPlayer("file.txt", "utf-8")
        assert self.general_lines == subtitle.get_general_format()

    def test_tmplayer_set_from_general_format(self):
        test_data = [
            "00:01:00:Line 01|Line 02",
            "00:01:03:Line 03|Line 04",
            "00:01:05:Line 04"
        ]
        subtitle = sublib.TMPlayer()
        subtitle.set_from_general_format(self.general_lines)
        assert test_data == subtitle.content
