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
print(Attractions)

Accommodation = pd.read_csv("Accommodation.csv")
Accommodation = pd.DataFrame(data=Accommodation)
print(Accommodation)

Activities = pd.read_csv("Activities.csv")
Activities = pd.DataFrame(data=Activities)
print(Activities)

print("next")
df = pd.merge(Accommodation, Attractions,how='inner', on='AddressRegion')
print(df)