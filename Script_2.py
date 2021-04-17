import csv, sys
import urllib3
import tkinter as tk
import pandas as pd
from tkinter import filedialog
from tkinter import *
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import plotly.graph_objects as go
import json
import urllib.request
import googlemaps
from itertools import tee
from dash.exceptions import PreventUpdate

from pandas import DataFrame

Attractions = pd.read_csv("Attractions.csv")
Attractions = pd.DataFrame(data=Attractions)

Accommodation = pd.read_csv("Accommodation.csv")
Accommodation: DataFrame = pd.DataFrame(data=Accommodation)

Activities = pd.read_csv("Activities.csv")
Activities = pd.DataFrame(data=Activities)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

##################### Histogram ########################################
# fig = px.bar(Accommodation, x="AddressRegion", y="count(pd.groupby(AddressRegion))", color="City", barmode="group")

### MAPS
def read_geojson(url):
    with urllib.request.urlopen(url) as url:
        jdata = json.loads(url.read().decode())
    return jdata


irish_url = 'https://gist.githubusercontent.com/pnewall/9a122c05ba2865c3a58f15008548fbbd/raw' \
            '/5bb4f84d918b871ee0e8b99f60dde976bb711d7c/ireland_counties.geojson '

geojson = read_geojson(irish_url)

## Attractions DF
Attractions = pd.read_csv("Attractions.csv")
Attractions = pd.DataFrame(data=Attractions)

Attractions.drop("Url", inplace=True, axis=1)
Attractions.drop('Tags', inplace=True, axis=1)
Attractions.drop("Longitude", inplace=True, axis=1)
Attractions.drop('Latitude', inplace=True, axis=1)
Attractions.drop("AddressLocality", inplace=True, axis=1)
Attractions.drop('AddressCountry', inplace=True, axis=1)
Attractions.drop('Telephone', inplace=True, axis=1)

Attractions['Type'] = 'Attraction'

## Accommodation DF
Accommodation = pd.read_csv("Accommodation.csv")
Accommodation = pd.DataFrame(data=Accommodation)

Accommodation.drop("Url", inplace=True, axis=1)
Accommodation.drop('Tags', inplace=True, axis=1)
Accommodation.drop("Longitude", inplace=True, axis=1)
Accommodation.drop('Latitude', inplace=True, axis=1)
Accommodation.drop("AddressLocality", inplace=True, axis=1)
Accommodation.drop('AddressCountry', inplace=True, axis=1)
Accommodation.drop('Telephone', inplace=True, axis=1)

Accommodation['Type'] = 'Accommodation'

## Activities DF
Activities = pd.read_csv("Activities.csv")
Activities = pd.DataFrame(data=Activities)

Activities.drop("Url", inplace=True, axis=1)
Activities.drop('Tags', inplace=True, axis=1)
Activities.drop("Longitude", inplace=True, axis=1)
Activities.drop('Latitude', inplace=True, axis=1)
Activities.drop("AddressLocality", inplace=True, axis=1)
Activities.drop('AddressCountry', inplace=True, axis=1)
Activities.drop('Telephone', inplace=True, axis=1)

Activities['Type'] = 'Activities'

## Merging Dataframes
new1 = Accommodation.append(Activities, ignore_index=True)
final = new1.append(Attractions, ignore_index=True)
df2 = px.data.election()
df = final
Types = df.Type.unique()

county_options = df['AddressRegion'].unique().tolist()
# histogram_df = rbind()
fig2 = px.histogram(Accommodation, x="AddressRegion",color="Type")

app.layout = html.Div(children=[
    html.H1(children='My First Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
    html.Div([
        dcc.Dropdown(id="County",options=[{'label': i,'value': i} for i in county_options],value='value'),
        dcc.Dropdown(id="my_dynamic_dropdown"),],
        style={'width': '25%','display': 'inline-block'}),

    dcc.Graph(
        id='example-graph',
        figure= fig2
    ),
    html.Div([
    dcc.Graph(
       id='example-graph2',
    )],),
    html.Div([
    html.P("Type:"),
        dcc.RadioItems(
            id='Type',
            options=[{'value': x, 'label': x}
                    for x in Types],
            value=Types[0],
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Graph(id="choropleth"),])


])

### DRIVE TIMES

# Perform request to use the Google Maps API web service
API_key = 'AIzaSyB6MeOpXZFeX70bKnZshD3q27KL3GHYqec'  # enter Google Maps API key
gmaps = googlemaps.Client(key=API_key)
origins = (53.00976, -6.29173)
destination = (53.34167, -6.25003)
result = gmaps.distance_matrix(origins, destination, mode='walking')

@app.callback(
    dash.dependencies.Output("my_dynamic_dropdown", "options"),
    [dash.dependencies.Input("County", "value")],
)
def update_options(County):
    data = df[df["AddressRegion"]==County]
    row_names = data["Name"].unique().tolist()
    lst = [{'label': i, 'value': i} for i in row_names]
    return lst

@app.callback(
    dash.dependencies.Output("example-graph2", "figure"),
    [dash.dependencies.Input("County", "value")],
    [dash.dependencies.Input("my_dynamic_dropdown", "value")],
)
def update_options(County,my_dynamic_dropdown):
    data = Accommodation[Accommodation["AddressRegion"]==County]# & Accommodation["Name"]==my_dynamic_dropdown]
    data = data[data["Name"]==my_dynamic_dropdown]
    #print(data)
    #row_names = data["Name"].unique().tolist()
    #fig=px.histogram(data, x = "AddressRegion")
    county_options = Accommodation["AddressRegion"].unique()
    # histogram_df = rbind()
    fig = px.histogram(data, x="AddressRegion")
    return fig

@app.callback(
    dash.dependencies.Output("choropleth", "figure"),
    [dash.dependencies.Input("Type", "value")])
def display_choropleth(Type):
    mapboxt = open("mapbox_token.txt").read().rstrip()
    data = df[df["Type"]==Type]
    print(data)
    counts = data['AddressRegion'].value_counts()
    county_names = counts.index.array
    print(df['AddressRegion'].unique())
    fig = go.Figure(go.Choroplethmapbox(z=counts,  # This is the data.
                                                  locations=county_names,
                                                  colorscale='blues',
                                                  colorbar=dict(thickness=20, ticklen=3),
                                                  geojson=geojson,
                                                  text=county_names,
                                                  hoverinfo='all',
                                                  marker_line_width=1, marker_opacity=0.75))
    fig.update_layout(title_text='Update Map',
                                title_x=0.5, width=700, height=700,
                                mapbox=dict(center=dict(lat=53.425049, lon=-7.944620),
                                            accesstoken=mapboxt,
                                            style='basic',
                                            zoom=5.6,
                                            ))
    return fig
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)