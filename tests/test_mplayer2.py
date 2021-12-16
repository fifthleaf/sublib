import unittest as ut
from unittest.mock import patch, mock_open
import datetime

import sublib as sbl


class MPlayer2ClassTest(ut.TestCase):

    def setUp(self):
        self.general_lines = [
            [datetime.timedelta(seconds=60, microseconds=100000), datetime.timedelta(seconds=63, microseconds=100000), 'Line 01|Line 02'],
            [datetime.timedelta(seconds=63, microseconds=300000), datetime.timedelta(seconds=65, microseconds=400000), 'Line 03|Line 04'],
            [datetime.timedelta(seconds=65, microseconds=600000), datetime.timedelta(seconds=66, microseconds=800000), 'Line 04']
        ]

    def test_get_general_format(self):
        format_lines = "[601][631] Line 01|Line 02\n[633][654] Line 03|Line 04\n[656][668] Line 04\n"
        with patch("builtins.open", mock_open(read_data=format_lines)) as mock_file:
            subtitle = sbl.MPlayer2(mock_file, "utf-8")
        self.assertEqual(self.general_lines, subtitle.get_general_format())

    def test_set_from_general_format(self):
        format_lines = ["[601][631] Line 01|Line 02", "[633][654] Line 03|Line 04", "[656][668] Line 04"]
        subtitle = sbl.MPlayer2()
        subtitle.set_from_general_format(self.general_lines)
        self.assertEqual(format_lines, subtitle.content)
