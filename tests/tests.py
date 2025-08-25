"""
Copyright IBM All Rights Reserved.

SPDX-License-Identifier: Apache-2.0
"""

import unittest

from datetime import datetime

from apptio_lib import apptio
from apptio_lib import cloudability as cldy

class TestFormatFiscalDate(unittest.TestCase):
    def test_default_fiscal_year_start(self):
        self.assertEqual(apptio.format_fiscal_date("2023-06-15"), "Jun:FY2023")
        self.assertEqual(apptio.format_fiscal_date("2023-01-01"), "Jan:FY2023")
        self.assertEqual(apptio.format_fiscal_date("2023-12-31"), "Dec:FY2023")

    def test_custom_fiscal_year_start(self):
        self.assertEqual(apptio.format_fiscal_date("2023-11-01", year_start=10), "Nov:FY2024")
        self.assertEqual(apptio.format_fiscal_date("2023-10-01", year_start=10), "Oct:FY2024")
        self.assertEqual(apptio.format_fiscal_date("2023-09-30", year_start=10), "Sep:FY2023")
        self.assertEqual(apptio.format_fiscal_date("2023-12-25", year_start=12), "Dec:FY2024")

    def test_datetime_object_input(self):
        # Test with a datetime object
        dt_obj = datetime(2023, 7, 20)
        self.assertEqual(apptio.format_fiscal_date(dt_obj), "Jul:FY2023")
        dt_obj_fy_change = datetime(2023, 8, 15)
        self.assertEqual(apptio.format_fiscal_date(dt_obj_fy_change, year_start=8), "Aug:FY2024")

    def test_invalid_date_format(self):
        self.assertIsNone(apptio.format_fiscal_date("2023/06/15"))

        self.assertIsNone(apptio.format_fiscal_date("not-a-date"))

if __name__ == '__main__':
    unittest.main()