import unittest
import sys
import os
from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(__file__)), 'src'))
from ghrs import GHRS


class TestData(unittest.TestCase):

    def setUp(self):

        self.obj = GHRS()

    def tearDown(self):

        del self.obj

    def test_authenticate(self):
        self.assertEqual(self.obj.response.status_code, 200)


    def test_get_recent_data(self):
        
        df = self.obj.get_recent_data('F94170', '102')
        self.assertEqual(isinstance(df, pd.DataFrame), True)
        self.assertGreater(len(df), 1)


