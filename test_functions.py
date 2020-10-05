"""
tests for bokeh_prophet scripts
"""

import pytest
import pandas as pd
from bokeh_prophet import preprocessing
from prophet_countries_forecast import forecast_preprocessing, forecast_postprocessing

DATA = './data/all_country_temp_data_CLEAN.csv'
SHAPEFILE = './data/ne_110m_admin_0_countries.shp'
FC = './data/country_forecast.csv'

def test_number_countries():
    df = preprocessing(DATA, FC)
    assert len(df['country'].unique()) == 236

def test_forecast_preprocessing():
    data = forecast_preprocessing(DATA)
    country_list = data['country'].unique()
    assert len(country_list) == 236
