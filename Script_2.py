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
county_options = Accommodation["AddressRegion"].unique()
# histogram_df = rbind()
fig2 = px.histogram(Accommodation, x="AddressRegion")


# df = pd.merge(Accommodation, Attractions,how='inner', on='AddressRegion')
# df = Accommodation.merge(Attractions, on = 'AddressRegion').merge(Activities, on = 'AddressRegion')
# print(df)

### MAPS
def read_geojson(url):
    with urllib.request.urlopen(url) as url:
        jdata = json.loads(url.read().decode())
    return jdata


irish_url = 'https://gist.githubusercontent.com/pnewall/9a122c05ba2865c3a58f15008548fbbd/raw' \
            '/5bb4f84d918b871ee0e8b99f60dde976bb711d7c/ireland_counties.geojson '

jdata = read_geojson(irish_url)

thelist = jdata['features']

counts = Accommodation['AddressRegion'].value_counts()
county_names = counts.index.array

mapboxt = open("mapbox_token.txt").read().rstrip()  # my mapbox_access_token  must be used only for special mapbox style
print('mapboxt: ', mapboxt)

fig_accommodation = go.Figure(go.Choroplethmapbox(z=counts,  # This is the data.
                                                  locations=county_names,
                                                  colorscale='blues',
                                                  colorbar=dict(thickness=20, ticklen=3),
                                                  geojson=jdata,
                                                  text=county_names,
                                                  hoverinfo='all',
                                                  marker_line_width=1, marker_opacity=0.75))

fig_accommodation.update_layout(title_text='Accommodation',
                                title_x=0.5, width=700, height=700,
                                mapbox=dict(center=dict(lat=53.425049, lon=-7.944620),
                                            accesstoken=mapboxt,
                                            style='basic',
                                            zoom=5.6,
                                            ))

app.layout = html.Div(children=[
    html.H1(children='My First Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
    html.Div([
        dcc.Dropdown(id="County",options=[{'label': i,'value': i} for i in county_options],value='value'),
        dcc.Dropdown(id="my-dynamic-dropdown"),],
        style={'width': '25%','display': 'inline-block'}),

    dcc.Graph(
        id='example-graph',
        figure= fig2
    ),
    dcc.Graph(
        id='example-graph2',
    ),

    dcc.Graph(
        id='fig_accommodation',
        figure=fig_accommodation
    )
    # dcc.Graph(id='funnel-graph'),
])

### DRIVE TIMES

# Perform request to use the Google Maps API web service
API_key = 'AIzaSyB6MeOpXZFeX70bKnZshD3q27KL3GHYqec'  # enter Google Maps API key
gmaps = googlemaps.Client(key=API_key)
origins = (53.00976, -6.29173)
destination = (53.34167, -6.25003)
result = gmaps.distance_matrix(origins, destination, mode='walking')

@app.callback(
    dash.dependencies.Output("my-dynamic-dropdown", "options"),
    [dash.dependencies.Input("County", "value")],
)
def update_options(search_value):
    data = Accommodation[Accommodation["AddressRegion"]==search_value]
    row_names = data["Name"].unique().tolist()
    lst = [{'label': i, 'value': i} for i in row_names]
    return lst

@app.callback(
    dash.dependencies.Output("example-graph2", "fig_3"),
    [dash.dependencies.Input("County", "value")],
    [dash.dependencies.Input("my-dynamic-dropdown", "search_value")],
)
def update_options(search_value,value):
    if not search_value:
        raise PreventUpdate
    if not value:
        raise PreventUpdate
    data = Accommodation[Accommodation["AddressRegion"]==value & Accommodation["Name"]==search_value]
    row_names = data["Name"].unique().tolist()
    lst = [{'label': i, 'value': i} for i in row_names]
    return  dcc.Graph(
        id='average_country',
        figure={
        'data': [{'x': lst,'type': 'histogram'
        }]})

# @app.callback(
#     dash.dependencies.Output('example-graph', fig2),
#     [dash.dependencies.Input('County', 'value')])
# def update_graph(County):
#     if County == "All Counties":
#         df_plot = Accommodation.copy()
#     else:
#         df_plot = Accommodation[Accommodation['AddressRegion'] == County]
#
#     pv = pd.pivot_table(
#         df_plot,
#         index=['AddressRegion'],
#         aggfunc=sum)
#     fig2 = px.histogram(pv)


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)