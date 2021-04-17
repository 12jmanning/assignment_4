import urllib
########### Python 3.2 #############
import json
import urllib
########### Python 3.2 #############
import urllib.error
import urllib.parse
import urllib.request
import urllib.request
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import plotly.graph_objects as go
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

token = open("mapbox_token.txt").read()  # you will need your own token


### MAPS
def read_geojson(url):
    with urllib.request.urlopen(url) as url:
        geojson = json.loads(url.read().decode())
    return geojson


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

app = dash.Dash(__name__)

app.layout = html.Div([
    html.P("Type:"),
    dcc.RadioItems(
        id='Type',
        options=[{'value': x, 'label': x}
                 for x in Types],
        value=Types[0],
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id="choropleth"),
])


@app.callback(
    Output("choropleth", "figure"),
    [Input("Type", "value")])
def display_choropleth(Type):
    mapboxt = open("mapbox_token.txt").read().rstrip()
    data = df[df["Type"]==Type]
    print(data)
    counts = data['AddressRegion'].value_counts()
    county_names = counts.index.array
    print(counts)
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
    #fig = px.choropleth_mapbox(
     #   z=counts, geojson=geojson, color='AddressRegion',
      #  locations=county_names, featureidkey="properties.district",
       # center={"lat": 53.425049, "lon": -7.944620}, zoom=9,
        #range_color=[0, 6500])
    #fig.update_layout(
     #   margin={"r": 0, "t": 0, "l": 0, "b": 0},
      #  mapbox_accesstoken=token)

    return fig


app.run_server(debug=True)
