import unittest as ut
from unittest.mock import patch, mock_open
import datetime

import sublib as sbl


class SubRipClassTest(ut.TestCase):

    def setUp(self):
        self.general_lines = [
            [datetime.timedelta(seconds=60, microseconds=60000), datetime.timedelta(seconds=63, microseconds=105000), 'Line 01|Line 02'],
            [datetime.timedelta(seconds=63, microseconds=272000), datetime.timedelta(seconds=65, microseconds=440000), 'Line 03|Line 04'],
            [datetime.timedelta(seconds=65, microseconds=607000), datetime.timedelta(seconds=66, microseconds=775000), 'Line 04']
        ]

    def test_get_general_format(self):
        format_lines = "1\n00:01:00,060 --> 00:01:03,105\nLine 01\nLine 02\n\n2\n00:01:03,272 --> 00:01:05,440\nLine 03\nLine 04\n\n3\n00:01:05,607 --> 00:01:06,775\nLine 04\n\n"
        with patch("builtins.open", mock_open(read_data=format_lines)) as mock_file:
            subtitle = sbl.SubRip(mock_file, "utf-8")
        self.assertEqual(self.general_lines, subtitle.get_general_format())

    def test_set_from_general_format(self):
        format_lines = ["1\n00:01:00,060 --> 00:01:03,105\nLine 01\nLine 02\n", "2\n00:01:03,272 --> 00:01:05,440\nLine 03\nLine 04\n", "3\n00:01:05,607 --> 00:01:06,775\nLine 04\n"]
        subtitle = sbl.SubRip()
        subtitle.set_from_general_format(self.general_lines)
        self.assertEqual(format_lines, subtitle.content)
