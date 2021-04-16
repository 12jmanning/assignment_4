import csv, sys
import urllib3
import tkinter as tk
import pandas as pd
from tkinter import filedialog
from tkinter import *
import pandas as pd
import numpy as np
########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json

Attractions = pd.read_csv("Attractions.csv")
Attractions = pd.DataFrame(data=Attractions)

Accommodation = pd.read_csv("Accommodation.csv")
Accommodation = pd.DataFrame(data=Accommodation)

Activities = pd.read_csv("Activities.csv")
Activities = pd.DataFrame(data=Activities)

#df = pd.merge(Accommodation, Attractions,how='inner', on='AddressRegion')
#df = Accommodation.merge(Attractions, on = 'AddressRegion').merge(Activities, on = 'AddressRegion')
#print(df)