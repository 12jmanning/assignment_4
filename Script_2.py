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

Attractions = pd.read_csv("Attractions.csv")
Attractions = pd.DataFrame(data=Attractions)

Accommodation = pd.read_csv("Accommodation.csv")
Accommodation = pd.DataFrame(data=Accommodation)

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

fig = px.bar(Accommodation, x="AddressRegion", y="count(pd.groupby(AddressRegion))", color="City", barmode="group")
fig2 = px.histogram(Accommodation, x ="AddressRegion", type = "histogram")

app.layout = html.Div(children=[
    html.H1(children='My First Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig2
    )
])

    
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)



#df = pd.merge(Accommodation, Attractions,how='inner', on='AddressRegion')
#df = Accommodation.merge(Attractions, on = 'AddressRegion').merge(Activities, on = 'AddressRegion')
#print(df)