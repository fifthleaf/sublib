import unittest as ut
from unittest.mock import patch, mock_open

import sublib as sbl


class DetectFuncTest(ut.TestCase):

    def test_mpl(self):
        test_data = "[601][631] Line 01|Line 02\n[633][654] Line 03|Line 04\n[656][668] Line 04\n"
        with patch("builtins.open", mock_open(read_data=test_data)) as mock_file:
            self.assertEqual("mpl", sbl.detect(mock_file, "utf-8"))
            self.assertNotEqual("srt", sbl.detect(mock_file, "utf-8"))
            self.assertNotEqual("sub", sbl.detect(mock_file, "utf-8"))
            self.assertNotEqual("tmp", sbl.detect(mock_file, "utf-8"))
            self.assertNotEqual("undefined", sbl.detect(mock_file, "utf-8"))

    def test_srt(self):
        test_data = "1\n00:01:00,060 --> 00:01:03,105\nLine 01\nLine 02\n\n2\n00:01:03,272 --> 00:01:05,440\nLine 03\nLine 04\n\n3\n00:01:05,607 --> 00:01:06,775\nLine 04\n\n"
        with patch("builtins.open", mock_open(read_data=test_data)) as mock_file:
            self.assertNotEqual("mpl", sbl.detect(mock_file, "utf-8"))
            self.assertEqual("srt", sbl.detect(mock_file, "utf-8"))
            self.assertNotEqual("sub", sbl.detect(mock_file, "utf-8"))
            self.assertNotEqual("tmp", sbl.detect(mock_file, "utf-8"))
            self.assertNotEqual("undefined", sbl.detect(mock_file, "utf-8"))

    def test_sub(self):
        test_data = "{1440}{1513}Line 01|Line 02\n{1517}{1569}Line 03|Line 04\n{1573}{1601}Line 04\n"
        with patch("builtins.open", mock_open(read_data=test_data)) as mock_file:
            self.assertNotEqual("mpl", sbl.detect(mock_file, "utf-8"))
            self.assertNotEqual("srt", sbl.detect(mock_file, "utf-8"))
            self.assertEqual("sub", sbl.detect(mock_file, "utf-8"))
            self.assertNotEqual("tmp", sbl.detect(mock_file, "utf-8"))
            self.assertNotEqual("undefined", sbl.detect(mock_file, "utf-8"))

    def test_tmp(self):
        test_data = "00:01:00:Line 01|Line 02\n00:01:03:Line 03|Line 04\n00:01:05:Line 04"
        with patch("builtins.open", mock_open(read_data=test_data)) as mock_file:
            self.assertNotEqual("mpl", sbl.detect(mock_file, "utf-8"))
            self.assertNotEqual("srt", sbl.detect(mock_file, "utf-8"))
            self.assertNotEqual("sub", sbl.detect(mock_file, "utf-8"))
            self.assertEqual("tmp", sbl.detect(mock_file, "utf-8"))
            self.assertNotEqual("undefined", sbl.detect(mock_file, "utf-8"))

    def test_false(self):
        test_data = "Line 01\nLine 02\nLine 03"
        with patch("builtins.open", mock_open(read_data=test_data)) as mock_file:
            self.assertNotEqual("mpl", sbl.detect(mock_file, "utf-8"))
            self.assertNotEqual("srt", sbl.detect(mock_file, "utf-8"))
            self.assertNotEqual("sub", sbl.detect(mock_file, "utf-8"))
            self.assertNotEqual("tmp", sbl.detect(mock_file, "utf-8"))
            self.assertEqual("undefined", sbl.detect(mock_file, "utf-8"))
