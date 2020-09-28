import pytest

class Prediction_tests:

	def number_countries(self):
		countires = './data/all_country_temp_data_CLEAN.csv'
		fc = './data/country_forecast.csv'
		assert len(countries['country'].unique())==len(fc['country'].unique())

	def years_of_prediction(self):
		fc = './data/country_forecast.csv'
		assert len(fc['year'].unique())==20
