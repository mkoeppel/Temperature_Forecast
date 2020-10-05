import pytest
import pandas as pd
from prophet_countries_forcast import forecast_postprocessing


def years_of_prediction(fc):
    fc = forecast_postprocessing(results)
    assert len(fc['year'].unique()) == 20
