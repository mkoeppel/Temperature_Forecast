[![Build Status](https://travis-ci.org/mkoeppel/Temperature_Forecast.svg?branch=master)](https://travis-ci.org/mkoeppel/Temperature_Forecast)

# Temperature_Forecast
Interactive forecast of global temperature development

## Disclaimer: this is NOT a sophisticted model of world-wide temperature change!

This forecast is using fb.prophet to forecast countries temperatures on a 240 month (20 years) scale and display these as an interactive map.
The data for this particular project was scraped from Berkeley Earth and cleaned / pre-processed (For which I would like to thank and acknowledge Paul Wlodkowski @github.com/pawlodkowski).

The forecasting algorithm was applied to individual countries contained in the Berkeley dataset and resulted in monthly predictions of that countries temperature.
Subsequently, the mean per year was calculated and coupled a GeoJSON file to allow for display on a map.
Finally Bokeh was used to obtain an interactive map in which individual years and countries can be selected/ highlighted.

To get to the map, download the data/ folder and 'prophet_countries_forcast.py' and 'bokeh_prophet.py'. After running 'prophet_countries_forcast.py'
a html-site with the map can be obtained by typing into a terminal: bokeh serve --show bokeh_prophet.py
