import unittest as ut
from unittest.mock import patch, mock_open
import datetime

import sublib as sbl


class MicroDVDClassTest(ut.TestCase):

    def setUp(self):
        self.general_lines = [
            [datetime.timedelta(seconds=60, microseconds=60000), datetime.timedelta(seconds=63, microseconds=105000), 'Line 01|Line 02'],
            [datetime.timedelta(seconds=63, microseconds=272000), datetime.timedelta(seconds=65, microseconds=440000), 'Line 03|Line 04'],
            [datetime.timedelta(seconds=65, microseconds=607000), datetime.timedelta(seconds=66, microseconds=775000), 'Line 04']
        ]

    def test_get_general_format(self):
        format_lines = "{1440}{1513}Line 01|Line 02\n{1517}{1569}Line 03|Line 04\n{1573}{1601}Line 04\n"
        with patch("builtins.open", mock_open(read_data=format_lines)) as mock_file:
            subtitle = sbl.MicroDVD(mock_file, "utf-8")
        self.assertEqual(self.general_lines, subtitle.get_general_format())

    def test_set_from_general_format(self):
        format_lines = ["{1440}{1513}Line 01|Line 02", "{1517}{1569}Line 03|Line 04", "{1573}{1601}Line 04"]
        subtitle = sbl.MicroDVD()
        subtitle.set_from_general_format(self.general_lines)
        self.assertEqual(format_lines, subtitle.content)
