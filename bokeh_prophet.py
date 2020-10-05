#!/usr/bin/env python
# coding: utf-8

# - **CREDITS**:
#     - This is an adapted script from [Paul Wlodkowski](https://github.com/pawlodkowski) for the *Plotting on Maps* lesson @ Spiced Academy.
#     - The data for this particular lesson was scraped from [Berkeley Earth](http://berkeleyearth.lbl.gov/country-list/) pre-processed.

import pandas as pd
import geopandas as gpd

from bokeh.plotting import figure
from bokeh.io import output_notebook, show
from bokeh.models import GeoJSONDataSource
from bokeh.palettes import brewer
from bokeh.models import LinearColorMapper
from bokeh.models import ColorBar, HoverTool
from bokeh.models import Slider
from bokeh.layouts import widgetbox, column
from bokeh.io import curdoc


######### Paths to datafiles:
DATA = './data/all_country_temp_data_CLEAN.csv'
SHAPEFILE = './data/ne_110m_admin_0_countries.shp'
FC = './data/country_forecast.csv'

######### used functions:
def preprocessing(DATA, FC):
    """
    reads the input tables and concatenates a complete dataframe used for visualization

    Params:
        input: takes 2 csv-files with country-names, years, and (forecasted) temperature-changes
        output: one dataframe with alle temperature-changes for each country and year
    """
    countries = pd.read_csv(DATA)
    countries = countries.loc[countries['country'] != 'Antarctica']
    countries = countries.groupby(['country', 'year'])[['monthly_anomaly']].mean().reset_index()
    fc = pd.read_csv(FC)
    df = pd.concat([countries, fc])
    return df

def get_geojson(yr):
    """Input a year (int) and return corresponding GeoJSON"""
    gdf_year = gdf_merged[gdf_merged['year'] == yr]
    return gdf_year.to_json()

def update_plot(attr, old, new):

    """Change properties / attributes of the datasource and title depending on slider value / position."""

    yr = slider.value
    new_data = get_geojson(yr) #our custom function from before
    geosource.geojson = new_data
    p.title.text = f'Avg. Monthly Temperature Anomaly for Year {yr}'


######### file processing:
df = preprocessing(DATA, FC)

gdf = gpd.read_file(SHAPEFILE)[['ADMIN', 'geometry']]
gdf_merged = pd.merge(left = gdf, right = df, left_on = 'ADMIN', right_on = 'country')
gdf_merged['monthly_anomaly'].min()
gdf_2000 = gdf_merged[gdf_merged['year'] == 2019]

geosource = GeoJSONDataSource(geojson = get_geojson(2019))


######### plotting
hover = HoverTool(tooltips = [ ('Country','@country'), ('Temp. Anomaly', '@monthly_anomaly')])

slider = Slider(title = 'Year', start = 1900, end = 2032, step = 1, value = 2013)

p = figure(title = 'Avg. Monthly Temperature Anomaly for Year 1900',
           plot_height = 600,
           plot_width = 900,
           tools=[hover]
          )

p.tools.append(hover)

palette = brewer['RdBu'][11]

color_mapper = LinearColorMapper(palette = palette,
                                 low = -3.5,
                                 high = 3.5,
                                 nan_color = 'cornflowerblue')

color_bar = ColorBar(color_mapper = color_mapper,
                     label_standoff = 8,
                     width =  500,
                     height = 20,
                     location = (0,0),
                     orientation = 'horizontal'
                    )

p.patches('xs',
          'ys',
          source = geosource,
          fill_color = {'field' :'monthly_anomaly', 'transform': color_mapper}, ### NEW ###
          line_color = 'blue',
          line_width = 1)

p.add_layout(color_bar, 'below')

slider.on_change('value', update_plot)

layout = column(p,widgetbox(slider))
curdoc().add_root(layout)

# **To view this application in interactive mode you need to set up a local Bokeh server.**
#
# **In the terminal, run:**
#
# bokeh serve --show bokeh_prophet.py
