import pytest
import pandas

class PredictionTests:

	def number_countries(self):
		countries = pd.read_csv('./data/all_country_temp_data_CLEAN.csv')
		fc = pd.read_csv('./data/country_forecast.csv')
		assert len(countries['country'].unique())==len(fc['country'].unique())

	def years_of_prediction(self):
		fc = pd.read_csv('./data/country_forecast.csv')
		assert len(fc['year'].unique())==20
