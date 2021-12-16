import unittest as ut
from unittest.mock import patch, mock_open
import datetime

import sublib as sbl


class TMPlayerClassTest(ut.TestCase):

    def setUp(self):
        self.general_lines = [
            [datetime.timedelta(seconds=60), datetime.timedelta(seconds=61), 'Line 01|Line 02'],
            [datetime.timedelta(seconds=63), datetime.timedelta(seconds=64), 'Line 03|Line 04'],
            [datetime.timedelta(seconds=65), datetime.timedelta(seconds=66), 'Line 04']
        ]

    def test_get_general_format(self):
        format_lines = "00:01:00:Line 01|Line 02\n00:01:03:Line 03|Line 04\n00:01:05:Line 04"
        with patch("builtins.open", mock_open(read_data=format_lines)) as mock_file:
            subtitle = sbl.TMPlayer(mock_file, "utf-8")
        self.assertEqual(self.general_lines, subtitle.get_general_format())

    def test_set_from_general_format(self):
        format_lines = ["00:01:00:Line 01|Line 02", "00:01:03:Line 03|Line 04", "00:01:05:Line 04"]
        subtitle = sbl.TMPlayer()
        subtitle.set_from_general_format(self.general_lines)
        self.assertEqual(format_lines, subtitle.content)
