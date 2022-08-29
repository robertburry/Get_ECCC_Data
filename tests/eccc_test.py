from unittest import TestCase
import pandas as pd

import get_eccc_data as ec


class import_station_list(TestCase):
    def test_is_df_with_data(self):
        s = ec.import_station_list()
        assert isinstance(s, pd.DataFrame) is True
        self.assertTrue(len(s) > 0)


class airport_search(TestCase):
    def test_is_df_with_data(self):
        url = 'https://drive.google.com/file/d/1HDRnj41YBWpMioLPwAFiLlK4SK8NV72C/view'
        url = 'https://drive.google.com/uc?id=' + url.split('/')[-2]
        df = pd.read_csv(url, skiprows=3)
        s = ec.airport_search('yyt', df)
        assert isinstance(s, pd.DataFrame) is True


class import_climate_data(TestCase):
    def test_is_df_with_data(self):
        s = ec.import_climate_data([2020], 8403505, 'NL')
        assert isinstance(s, pd.DataFrame) is True
        self.assertTrue(len(s) > 0)
