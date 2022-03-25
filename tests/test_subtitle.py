import builtins
import datetime

import pytest
import pytest_mock
import sublib


class TestSubtitleClass:

    @pytest.fixture
    def subtitle_empty(self):
        return sublib.Subtitle("file.txt", "utf-8")

    @pytest.fixture
    def subtitle_valid(self, mocker):
        mocker.patch(
            "builtins.open",
            mocker.mock_open(
                read_data="Line 01\nLine 02\n"
            )
        )
        return sublib.Subtitle("file.txt", "utf-8")

    def test_subtitle__init__(self, subtitle_empty, subtitle_valid):
        subtitle_1 = subtitle_empty
        subtitle_2 = subtitle_valid
        assert subtitle_1.content == []
        assert subtitle_2.path == "file.txt"
        assert subtitle_2.encoding == "utf-8"
        assert subtitle_2.content == ["Line 01", "Line 02"]

    def test_subtitle__str__(self):
        subtitle_1 = sublib.Subtitle()
        subtitle_2 = sublib.Subtitle("file.txt", "utf-8")
        assert str(subtitle_1) == 'Subtitle("", "")'
        assert str(subtitle_2) == 'Subtitle("file.txt", "utf-8")'

    def test_subtitle__repr__(self):
        subtitle_1 = sublib.Subtitle()
        subtitle_2 = sublib.Subtitle("file.txt", "utf-8")
        assert repr(subtitle_1) == 'Subtitle(path="", encoding="")'
        assert repr(subtitle_2) == 'Subtitle(path="file.txt", encoding="utf-8")'

    def test_subtitle__bool__(self, subtitle_empty, subtitle_valid):
        subtitle_1 = subtitle_empty
        subtitle_2 = subtitle_valid
        assert not bool(subtitle_1)
        assert bool(subtitle_2)

    def test_subtitle__eq__(self, subtitle_empty, subtitle_valid):
        subtitle_1 = subtitle_empty
        subtitle_2 = subtitle_valid
        subtitle_3 = subtitle_valid
        assert subtitle_1 != subtitle_2
        assert subtitle_2 == subtitle_3

    def test_subtitle__len__(self, subtitle_empty, subtitle_valid):
        subtitle_1 = subtitle_empty
        subtitle_2 = subtitle_valid
        assert len(subtitle_1) == 0
        assert len(subtitle_2) == 2

    def test_subtitle__contains__(self, subtitle_valid):
        subtitle = subtitle_valid
        assert "line" not in subtitle
        assert "Line" in subtitle

    def test_subtitle__iter__(self, subtitle_valid):
        subtitle = subtitle_valid
        assert iter(subtitle) == subtitle
        assert hasattr(subtitle, "_iterator")

    def test_subtitle__next__(self, subtitle_valid):
        subtitle = subtitle_valid
        iter(subtitle)
        assert next(subtitle) == "Line 01"
        assert next(subtitle) == "Line 02"
        with pytest.raises(IndexError):
            assert next(subtitle)
