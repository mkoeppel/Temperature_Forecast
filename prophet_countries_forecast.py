#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
from fbprophet import Prophet


DATA = './data/all_country_temp_data_CLEAN.csv'

def forecast_preprocessing(DATA):
    """
    preprocessing of Berkeley-data to be used for temperature prediction

    Params:
        input: takes the dataframe with monthly_anomaly per country
        output: a modified dataframe that can be used by subsequent functions
    """
    data = pd.read_csv(DATA)
    data['year_month'] = data.year.astype(str) + "-" + data.month.astype(str)
    data['date'] = pd.to_datetime(data['year_month'].astype(str), yearfirst = True)
    data = data.loc[data['country'] != 'Antarctica']
    data.dropna(inplace = True)
    return data

def select_and_process_country(country):
    '''
    processes the given countries according to the input needs of fbprophet

    Params:
        input: a list of countries as array (and the corresponding temperature dataframe from Berkeley)
        output: a dataframe that can be forwarded to fbprophet
    '''
    df = data.loc[data['country'] == country]
    df = df[['date', 'monthly_anomaly']]
    df = df.rename(columns={'date':'ds', 'monthly_anomaly':'y'})
    return df


def forecast_prophet(df):
    '''
    provides fbprophet temperature forecasts for periods (20 years) for the given country-df

    Params:
        input: a formatted dataframe with the date 'ds' and temperature-values as 'y'
        output: a forecast dataframe with the results (ds as date and trend as temp.-prediction)
    '''
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=240, freq='MS', include_history=False)
    forecast = m.predict(future)
    return forecast


data = forecast_preprocessing(DATA)
country_list = data['country'].unique()

collected_forecast = []
for country in country_list:
    df = select_and_process_country(country)
    forecast = forecast_prophet(df)
    result = forecast[['ds', 'trend']]
    result['country'] = country
    collected_forecast.append(result)
results = pd.concat(collected_forecast)

def forecast_postprocessing(results):
    """
    performs some clean-up of the data and prepares it for concatenation with inital make_future_dataframe

    Params:
        input: a concatenated dataframe of fb.prophet final_results
        output: a cleaned dataframe with newly labeled columns and yearly medians of forecasted temperature change
    """
    results['date'] = pd.to_datetime(results['ds'].astype(str), yearfirst = True)
    results['year'] = results['date'].dt.year
    results['month'] = results['date'].dt.month
    results = results[['country', 'trend', 'year', 'month']]
    results = results.loc[results['country'] != 'Antarctica']
    results = results.groupby(['country', 'year'])[['trend']].mean().reset_index()
    results.columns = ['country', 'year', 'monthly_anomaly']
    return results

final_results = forecast_postprocessing(results)
final_results.to_csv('./data/country_forecast.csv', sep=',', header=True,index=False)
