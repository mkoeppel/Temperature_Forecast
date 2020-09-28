import pytest

class Prediction_tests:

	def number_countries(self):
		assert len(countries['country'].unique())==len(fc['country'].unique())

	def years_of_prediction(self):
		assert len(fc['year'].unique())==20
