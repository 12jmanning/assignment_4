#Assignment 4 Script 2
#Adam Carty & Jack Manning


#Import Packages
import csv, sys
import urllib3
import tkinter as tk
import pandas as pd
from tkinter import filedialog
from tkinter import *
import numpy as np
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import plotly.graph_objects as go
import json
import urllib.request
import googlemaps
from itertools import tee
from dash.exceptions import PreventUpdate
import os
from pandas import DataFrame
import requests

#Read in Datasets
url = 'https://failteireland.azure-api.net/opendata-api/v1/accommodation/csv'
Attractions_new = pd.read_csv('https://failteireland.azure-api.net/opendata-api/v1/accommodation/csv')
#Read in Datasets
Attractions = pd.read_csv("Attractions.csv")
Attractions = pd.DataFrame(data=Attractions)
#Read in Datasets
Accommodation = pd.read_csv("Accommodation.csv")
Accommodation: DataFrame = pd.DataFrame(data=Accommodation)
#Read in Datasets
Activities = pd.read_csv("Activities.csv")
Activities = pd.DataFrame(data=Activities) 
#Include css stylesheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#Call external css stylesheet
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

### MAPS
#Function to read in url
def read_geojson(url):
    with urllib.request.urlopen(url) as url:
        jdata = json.loads(url.read().decode())
    return jdata

#Irish url created
irish_url = 'https://gist.githubusercontent.com/pnewall/9a122c05ba2865c3a58f15008548fbbd/raw' \
            '/5bb4f84d918b871ee0e8b99f60dde976bb711d7c/ireland_counties.geojson '
geojson = read_geojson(irish_url)
#Personal Google API Key
API_key = 'AIzaSyB6MeOpXZFeX70bKnZshD3q27KL3GHYqec'  # enter Google Maps API key

# covid DF
covid = pd.read_csv("Covid19CountyStatisticsHPSCIreland.csv")
covid = pd.DataFrame(data=covid)
## Attractions DF
Attractions = pd.read_csv("Attractions.csv")
Attractions = pd.DataFrame(data=Attractions)
Attractions['Type'] = 'Attraction'
## Accommodation DF
Accommodation = pd.read_csv("Accommodation.csv")
Accommodation = pd.DataFrame(data=Accommodation)
Accommodation['Type'] = 'Accommodation'
## Activities DF
Activities = pd.read_csv("Activities.csv")
Activities = pd.DataFrame(data=Activities)
Activities['Type'] = 'Activities'

## Merging Dataframes
new1 = Accommodation.append(Activities, ignore_index=True)
final = new1.append(Attractions, ignore_index=True)
df2 = px.data.election()
df = final
#Remove null values from dataframe
nan_value = "nan"
df.replace("", nan_value, inplace=True)
#Ensure all county names are capitalised and formatted correvtly
df.dropna(subset=["AddressRegion"], inplace=True)
df['AddressRegion'] = df['AddressRegion'].str.capitalize()
#Obtain a list of the 3 types: Attractions, Accomodation and Activities
Types = df.Type.unique()
#List of modes of transport as parameters for Google API
Modes = ('walking','driving','bicycling')
#Get list of unique county options
county_options = df['AddressRegion'].unique()
#Create an initial histogram of count by county (Address Region) coloured by type
fig2 = px.histogram(df, x="AddressRegion", color="Type")
#Creates an app and initialises it 
app.layout = html.Div(children=[
    #Initial text which describes the dashboard
    html.H1(children='Failte Ireland Dashboard'),

    html.Div(children="Welcome to Failte Ireland's Interactive Dashboard!"),
    html.Div(
        children="This dashboard incorporates the data of all of Faile Ireland's known accomodation, attractions and activities."),
    html.Div(
        children="You will be able to view each of these on the interactive map below. Also using the drop down boxes below, you can plan your next 'staycation'! "),
    html.Div(
        children="When planning this, you will be provided with the name, website and phone number of your selected value. "),
    html.Div(
        children="We also provide you with the historical COVID-19 case data for your selected county which will help you make informed decisions regarding your next staycation!"),
    #Heat map for the types by county
    html.Div([
        html.H2(children='Heatmap for Selected Type:'),
        html.P("Please Select one of the buttons below to update the map:"),
        #Radio buttons to allow the user to select specific types
        dcc.RadioItems(
            id='Type',
            #Options are populated by the pre defined list of types
            options=[{'value': x, 'label': x}
                     for x in Types],
            value=Types[0],
            labelStyle={'display': 'inline-block'}
        ),
        #Creates the graph and gives it an id reference to be called later
        dcc.Graph(id="choropleth"), ]),
    html.Div([
        #Sections to allow the user to explore types avalable by county and get details along with finding estimated travel times
        html.H2(children='Plan your next Trip!'),
        html.P(
            "Please Enter your address and preferred mode of transportation to find out your expected travel time."),
        html.P(""),
        #Input box to allow user to enter a starting point
        html.Div(["Your Address: ",
                  dcc.Input(id='my_input', value='initial value', type='text')]),
        html.Br(),
        html.P("Your Mode of Transport:"),
        #Dropdown list populated by the pre defined modes of transport the user can select
        dcc.Dropdown(id="mode_dropdown", options=[{'label': i, 'value': i} for i in Modes], value='value'),
        html.Br(),
        #Prints my_output
        html.Div(id='my_output'),
        html.Br(),
        html.P(
            "Please use the following dropdown lists to select your preferred county, activity, accomodation or attraction."),
        #Dropdown for all the counties in the dataset
        dcc.Dropdown(id="County", options=[{'label': i, 'value': i} for i in county_options], value='value'),
        #Dropdown for the three types in the dataset
        dcc.Dropdown(id="type_dropdown", options=[{'label': i, 'value': i} for i in Types], value='value'),
        #Dynamic dropdown which is populated based on parameters of other two dropdwns
        dcc.Dropdown(id="my_dynamic_dropdown"),
        html.Br(),
        #Prints out report details
        html.Div(id="report", children=""), 
        html.Br(),
        #Prints out travel time details
        html.Div(id='my_output2', children = "")],
        style={'width': '25%', 'display': 'inline-block'}),

    html.Div([
        #Graph of historical cumulative covid cases which is produced based on the selected county from the above dropdown list
        html.H2(children='Historical Cumulative COVID-19 Cases:'),
        html.P("See historical COVID-19 Cases in the county you have selected."),
        html.P(""),
        dcc.Graph(id='covid_graph', ), ]),

    html.Div([
        #Shows a break down of types by county in a histogram 
        html.H2(children='View Breakdown of Activities, Attractions and Accomodation by County!'),
        html.P("Please use the legend to the right of the graph to select Accomodation, Activities or Attractions."),
        html.P(""),
        dcc.Graph(
            id='example_graph',
            figure=fig2
        ), ]),

], )

### DRIVE TIMES

# Perform request to use the Google Maps API web service to find the expected travel time between the starting point and selected activity, accomodation or attraction by their preferred mode of travel
@app.callback(
    dash.dependencies.Output("my_output2", "children"),
    [dash.dependencies.Input("my_input", "value")],
    [dash.dependencies.Input("my_dynamic_dropdown", "value")],
    [dash.dependencies.Input("mode_dropdown", "value")],
)
def update_options(my_input, my_dynamic_dropdown,mode_dropdown):
    #only  updates if values are entered
    if my_dynamic_dropdown is None:
        raise PreventUpdate
    elif my_input is None:
        raise PreventUpdate
    elif mode_dropdown is None:
        raise PreventUpdate
    else:
        #Filter data based on input parameters
        origin_data = df[df["Name"] == my_dynamic_dropdown]
        #Extract destination longitude and latitude
        destination = (origin_data['Latitude'],origin_data['Longitude'])
        API_key = 'AIzaSyB6MeOpXZFeX70bKnZshD3q27KL3GHYqec'  # enter Google Maps API key
        #Address input as starting point
        address = my_input
        #initialise url and append the address and API key
        geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address={}".format(address)
        geocode_url = geocode_url + "&key={}".format(API_key)
        #enter key to access googlemaps API
        gmaps = googlemaps.Client(key=API_key)
        #request and extract results from the API
        results = requests.get(geocode_url)
        results = results.json()
        #Extract the longitude and latitude from the API results and enter into function to get expected travel time by transport mode selected
        origins = (results['results'][0]['geometry']['location']['lat'],results['results'][0]['geometry']['location']['lng'])
        result = gmaps.distance_matrix(origins, destination, mode=mode_dropdown)["rows"][0]["elements"][0]["duration"]["text"]
        result = "Your Expected travel time by "+mode_dropdown+" is "+result
        return result

#Fuction to update the dropdown list based on county and type selected in the other 2 dropdown boxes
@app.callback(
    dash.dependencies.Output("my_dynamic_dropdown", "options"),
    [dash.dependencies.Input("County", "value")],
    [dash.dependencies.Input("type_dropdown", "value")],
)
def update_options(County, type_dropdown):
    #filters data by county and type
    data = df[df["AddressRegion"] == County]
    data = data[data["Type"] == type_dropdown]
    #creates a unique list of names of the attractions, activities or accomodations
    row_names = data["Name"].unique().tolist()
    #returns list of name values
    lst = [{'label': i, 'value': i} for i in row_names]
    return lst

#creates a heat map from the value selected in the radio button
@app.callback(
    dash.dependencies.Output("choropleth", "figure"),
    [dash.dependencies.Input("Type", "value")])
def display_choropleth(Type):
    mapboxt = open("mapbox_token.txt").read().rstrip()
    #Data is filtered by type
    data = df[df["Type"] == Type]
    #Counts of each county are determined
    counts = data['AddressRegion'].value_counts()
    #Unique list of county names is made into an array
    county_names = counts.index.array
    #Creates a map and graphical representation based on filtered data
    fig = go.Figure(go.Choroplethmapbox(z=counts,  # This is the data.
                                        locations=county_names,
                                        colorscale='blues',
                                        colorbar=dict(thickness=20, ticklen=3),
                                        geojson=geojson,
                                        text=county_names,
                                        hoverinfo='all',
                                        marker_line_width=1, marker_opacity=0.75))
    fig.update_layout(
        title_x=0.5, width=700, height=700,
        mapbox=dict(center=dict(lat=53.425049, lon=-7.944620),
                    accesstoken=mapboxt,
                    style='basic',
                    zoom=5.6,
                    ))
    return fig


@app.callback(
    dash.dependencies.Output("covid_graph", "figure"),
    [dash.dependencies.Input("County", "value")])
def display_choropleth(County):
    #if no county is selected then the graph isnt drawn
    if County is None:
        raise PreventUpdate
    else:
        #Filter data by county
        data = covid[covid["CountyName"] == County]
        #Creates a bar chart of the filtered data over time
        fig = px.bar(data, x="TimeStamp", y="ConfirmedCovidCases")
        return fig


@app.callback(
    dash.dependencies.Output("report", "children"),
    [dash.dependencies.Input("County", "value")],
    [dash.dependencies.Input("type_dropdown", "value")],
    [dash.dependencies.Input("my_dynamic_dropdown", "value")])
def display_choropleth(County, type_dropdown, my_dynamic_dropdown):
    #If no values selected then don't update
    if my_dynamic_dropdown is None:
        raise PreventUpdate
    else:
        #Filter data by county, type and name
        data = df[df["AddressRegion"] == County]
        data = data[data["Type"] == type_dropdown]
        data = data[data["Name"] == my_dynamic_dropdown]
        #Build a string report of the details of the selected activity, attraction or accomodation
        my_report = ("Name: " + data["Name"] + "\n Website: " + data["Url"] + "\n Telephone: " + data[
            "Telephone"] + "\n County: " + data["AddressRegion"] + "\n")
        return my_report

#Method to print out the origin point as input by the user.
@app.callback(
    Output(component_id='my_output', component_property='children'),
    Input(component_id='my_input', component_property='value')
)
def update_output_div(input_value):
    return 'Origin (starting point): {}'.format(input_value)

#Main method called to run the script
if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=False)
