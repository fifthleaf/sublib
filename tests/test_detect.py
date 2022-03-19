import builtins

import pytest
import pytest_mock
import sublib


class TestDetectFunction:

    def test_detect_mpl_format(self, mocker):
        test_data = "[601][631] Line 01|Line 02\n"\
                    "[633][654] Line 03|Line 04\n"\
                    "[656][668] Line 04\n"
        mocker.patch(
            "builtins.open",
            mocker.mock_open(read_data=test_data)
        )
        assert "mpl" == sublib.detect("file.txt", "utf-8")
        assert "srt" != sublib.detect("file.txt", "utf-8")
        assert "sub" != sublib.detect("file.txt", "utf-8")
        assert "tmp" != sublib.detect("file.txt", "utf-8")
        assert "undefined" != sublib.detect("file.txt", "utf-8")

    def test_detect_srt_format(self, mocker):
        test_data = "1\n"\
                    "00:01:00,060 --> 00:01:03,105\n"\
                    "Line 01\n"\
                    "Line 02\n\n"\
                    "2\n"\
                    "00:01:03,272 --> 00:01:05,440\n"\
                    "Line 03\n"\
                    "Line 04\n\n"\
                    "3\n"\
                    "00:01:05,607 --> 00:01:06,775\n"\
                    "Line 04\n\n"
        mocker.patch(
            "builtins.open",
            mocker.mock_open(read_data=test_data)
        )
        assert "mpl" != sublib.detect("file.txt", "utf-8")
        assert "srt" == sublib.detect("file.txt", "utf-8")
        assert "sub" != sublib.detect("file.txt", "utf-8")
        assert "tmp" != sublib.detect("file.txt", "utf-8")
        assert "undefined" != sublib.detect("file.txt", "utf-8")

    def test_detect_sub_format(self, mocker):
        test_data = "{1440}{1513}Line 01|Line 02\n"\
                    "{1517}{1569}Line 03|Line 04\n"\
                    "{1573}{1601}Line 04\n"
        mocker.patch(
            "builtins.open",
            mocker.mock_open(read_data=test_data)
        )
        assert "mpl" != sublib.detect("file.txt", "utf-8")
        assert "srt" != sublib.detect("file.txt", "utf-8")
        assert "sub" == sublib.detect("file.txt", "utf-8")
        assert "tmp" != sublib.detect("file.txt", "utf-8")
        assert "undefined" != sublib.detect("file.txt", "utf-8")

    def test_detect_tmp_format(self, mocker):
        test_data = "00:01:00:Line 01|Line 02\n"\
                    "00:01:03:Line 03|Line 04\n"\
                    "00:01:05:Line 04\n"
        mocker.patch(
            "builtins.open",
            mocker.mock_open(read_data=test_data)
        )
        assert "mpl" != sublib.detect("file.txt", "utf-8")
        assert "srt" != sublib.detect("file.txt", "utf-8")
        assert "sub" != sublib.detect("file.txt", "utf-8")
        assert "tmp" == sublib.detect("file.txt", "utf-8")
        assert "undefined" != sublib.detect("file.txt", "utf-8")

    def test_detect_und_format(self, mocker):
        test_data = "Line 01\n"\
                    "Line 02\n"\
                    "Line 03\n"
        mocker.patch(
            "builtins.open",
            mocker.mock_open(read_data=test_data)
        )
        assert "mpl" != sublib.detect("file.txt", "utf-8")
        assert "srt" != sublib.detect("file.txt", "utf-8")
        assert "sub" != sublib.detect("file.txt", "utf-8")
        assert "tmp" != sublib.detect("file.txt", "utf-8")
        assert "undefined" == sublib.detect("file.txt", "utf-8")
