from pandas import json_normalize
import json
import streamlit as st
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
import time
from pprint import pprint
import json
from pandas import json_normalize
import pydeck as pdk

# Opening JSON file
f = open('location_history.json',)

# returns JSON object as
# a dictionary
data = json.load(f)
data = data["Areas you may have visited in the last two years"]
#print(data["Top Locations Per Six-Day Period"][0])


def focus_Date(text):
    text = text[:-13]
    return text


def focus_heure(text):
    text = text[11:-4]
    return text


def recup_lon(o):
    # instantiate a new Nominatim client
    app = Nominatim(user_agent="tp_Alex")
    # Now let's try to get geographic data from an address:

    # get location raw data
    location_1 = app.geocode(f"{o} +, France").raw
    # print raw data
    return location_1["lon"]


def recup_lat(o):
    # instantiate a new Nominatim client
    app = Nominatim(user_agent="tp_Alex")
    # Now let's try to get geographic data from an address:

    # get location raw data
    location_1 = app.geocode(f"{o} + , France").raw
    # print raw data
    return location_1["lat"]


list = [[], [], [], []]
i = 0

for period in data:
    i += 1
    list[0].append(recup_lon(period["City"]))
    list[1].append(recup_lat(period["City"]))
    list[2].append(focus_Date(period["Time"]))
    list[3].append(focus_heure(period["Time"]))
    if i >= 66:
        break

df = pd.DataFrame(list)
df = df.T
df.columns = ['lon', 'lat', 'Date', 'Time']
