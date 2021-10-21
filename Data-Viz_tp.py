from pandas.core.groupby.generic import DataFrameGroupBy
import altair as alt
from pandas import json_normalize
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim
import time
from pandas import json_normalize
import pydeck as pdk
import streamlit as st
from streamlit_folium import folium_static
import folium
from datetime import datetime, timedelta
from folium.plugins import MarkerCluster
import plotly.graph_objects as go
import plotly.express as px
plt.style.use('dark_background')
st.set_option('deprecation.showPyplotGlobalUse', False)


# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center; color: white;'>Did u borrow my snap account ?!</h1>",
            unsafe_allow_html=True)
st.markdown("<p style= color: white;'>Alexandre Messika - DS3</p>",
            unsafe_allow_html=True)
# Feature engineering

# df of recent locations
df = pd.read_csv('data.csv')
df = df.drop(columns='Unnamed: 0')
df_hour = pd.read_csv('data_time.csv')
df_hour = df_hour.drop(columns='Unnamed: 0')
df['DateTime'] = df['DateTime'].apply(
    lambda _: datetime.strptime(_, "%Y-%m-%d %H:%M:%S"))


# most used locations
map_data = pd.DataFrame(
    [[48.8356649, 2.240206, 'Boulogne'], [
        48.7921097, 2.3633048, 'Villejuif']],
    columns=['lat', 'lon', 'Best location'])

# df on weird values
select_df = df[['lat', 'lon']].copy()

foreign_df = df.mask(df['lat'] > 46)
foreign_df = foreign_df.dropna()
foreign_df_2 = df.mask(df['lon'] > 2.2)
foreign_df_2 = foreign_df_2.dropna()
foreign_df = pd.concat([foreign_df, foreign_df_2], ignore_index=True)
foreign_df.drop(7, inplace=True)

df_hacks = foreign_df.mask(foreign_df['lat'] < 38)
df_hacks = df_hacks.mask(df_hacks['lon'] < 1)
df_hacks = df_hacks.dropna()

nav = st.sidebar.radio(
    "Navigation", ["Investigation", "Plot analysis", "Mapping discovery", "Mapping investigation", "Conclusion"])

if nav == "Investigation":

    row1_1, row1_2, row1_3, row1_4, row1_5, row1_6 = st.columns((6))

    with row1_5:
        st.markdown('''
        <a href="https://www.linkedin.com/in/alexandre-messika-000708174/">
            <img src="https://i.ibb.co/XsqvvmB/LinkedIn.gif" width="100px" />
        </a>''',
                    unsafe_allow_html=True
                    )
    with row1_6:
        st.markdown('''
    <a href="https://github.com/AlexMessika?tab=repositories">
        <img src="https://i.ibb.co/sKBPNzC/Github.gif" width="100px"/>
    </a>''',
                    unsafe_allow_html=True
                    )
    st.write("  ")
    '''
    “Passwords are like underwear: don’t let people see it and never share it with strangers.” – Chris Pirillo'''
    st.image('téléchargement.jpg', width=800)


if nav == "Plot analysis":

    st.subheader("My most usual location")
    st.table(map_data)

    st.subheader("My Snapchat locations")
    df

    st.subheader('Check timeline')
    st.bar_chart(df['DateTime'])

    st.subheader("Identify weird locations")
    st.line_chart(select_df)

    st.subheader(
        "Create a mask which exclude average positions as u see therefore")
    fig, ax = plt.subplots(figsize=(4, 3))

    ax.scatter(y=(df['lon']+df['lat'])/2, x=df.index,
               s=20, facecolor='none', edgecolors='white')
    ax.plot([0, 5000], [25.55, 25.55], ':r')
    ax.plot([0, 5000], [30.20, 30.20], ':b')
    ax.set_ylabel('Position : avg(lon,lat)')
    ax.set_xlabel('Index values')

    plt.show()
    st.pyplot(fig)

    df_color = pd.DataFrame()
    df_color['loc'] = df['lon']*df['lat']
    df_color['color'] = 2
    fig = px.scatter(df_color, y="loc", x=df.index, color='color')
    fig.update_layout(
        dragmode="drawopenpath",
        newshape_line_color="cyan",
        title_text="Interactive visualization on strange values",
    )
    config = dict(
        {
            "scrollZoom": True,
            "displayModeBar": True,
            # 'editable'              : True,
            "modeBarButtonsToAdd": [
                "drawline",
                "drawopenpath",
                "drawclosedpath",
                "drawcircle",
                "drawrect",
                "eraseshape",
            ],
            "toImageButtonOptions": {"format": "svg"},
        }
    )
    st.plotly_chart(fig, config=config)

    st.subheader("Select foreign locations")
    foreign_df
    st.subheader('Verify vacation problem')
    st.bar_chart(foreign_df['DateTime'])
    st.subheader("Note that the potential hacking has a timeline spread mostly over the month of August 2021 and that part of it is due to a trip so let's see if other positions than Greece appear during this period... ")

    select_foreign_df = foreign_df[['lat', 'lon']].copy()
    st.line_chart(select_foreign_df)
    st.subheader(
        'Unless I have mastered teleportation, I think we have identified more precisely, one of the fraudulent connections')


if nav == "Conclusion":
    if st.checkbox('Show dataframe'):
        st.table(df)
    if st.checkbox('Show suspicious dataframe'):
        st.table(foreign_df)
    if st.checkbox('Show final suspicious dataframe'):
        st.table(df_hacks)


if nav == 'Mapping discovery':

    map_type = st.checkbox('Analyse suspicious point')
    row1_1, row1_2 = st.columns((2))

    with row1_1:
        st.subheader("All locations")
        fmap = folium.Map(location=[48.8534, 2.3488],
                          zoom_start=6, width=700, height=550)
        mCluster = folium.plugins.MarkerCluster(
            name="Markers").add_to(fmap)
        folium.TileLayer('cartodbdark_matter', name="dark mode",
                         control=True).add_to(fmap)
        rows, cols = df.shape
        for i in range(rows):
            marker = folium.Marker(
                location=[df['lat'][i], df['lon'][i]], tooltip=df['DateTime'][i])
            marker.add_to(mCluster)
        folium_static(fmap)
    with row1_2:

        if map_type:

            st.subheader("Now you can click on locations")
            map = folium.Map(location=[48.8534, 2.3488],
                             zoom_start=6, control_scale=True, width=700, height=550)
            folium.TileLayer('cartodbdark_matter', name="dark mode",
                             control=True).add_to(map)
            for row in foreign_df.index:
                folium.Marker([foreign_df['lat'].loc[row], foreign_df['lon'].loc[row]],
                              popup=foreign_df['DateTime'].loc[row]).add_to(map)
            folium_static(map)
        else:
            st.subheader("Suspicious locations in red")
            st.pydeck_chart(pdk.Deck(
                map_style='dark',
                initial_view_state=pdk.ViewState(
                    latitude=48.8534,
                    longitude=2.3488,
                    zoom=5,
                    pitch=50,
                    width=700,
                    height=510
                ),
                layers=[
                    pdk.Layer(
                        'ScatterplotLayer',
                        data=map_data,
                        get_position='[lon, lat]',
                        get_color='[132, 157, 60, 129]',
                        get_radius=4000,
                    ),
                    pdk.Layer(
                        "ColumnLayer",
                        data=map_data,
                        get_position="[lon, lat]",
                        get_elevation=2000,
                        elevation_scale=10,
                        radius=4000,
                        get_color='[255, 165, 0, 170]',
                        pickable=True,
                        auto_highlight=True,
                    ),
                    pdk.Layer(
                        'ScatterplotLayer',
                        data=foreign_df,
                        get_position="[lon, lat]",
                        get_color='[200, 30, 0, 160]',
                        get_radius=4000,
                    ),
                    pdk.Layer(
                        "ColumnLayer",
                        data=foreign_df,
                        get_position="[lon, lat]",
                        get_elevation=2000,
                        elevation_scale=10,
                        radius=4000,
                        get_color='[200, 30, 0, 160]',
                        pickable=True,
                        auto_highlight=True,
                    ),

                ],
            ))


if nav == 'Mapping investigation':

    # LOADING DATA

    for i in range(0, 4869):
        df['DateTime'].loc[i] = int(
            (((df['DateTime'].loc[i].timestamp() - (2021-1970)*365*24*60*60)/60)/60) % 24)

    # CREATING FUNCTION FOR MAPS

    def map(data, lat, lon, zoom):
        st.write(pdk.Deck(
            map_style="dark",
            initial_view_state={
                "latitude": lat,
                "longitude": lon,
                "zoom": zoom,
                "pitch": 50,
            },
            layers=[
                pdk.Layer(
                    "HexagonLayer",
                    data,
                    get_position=["lon", "lat"],
                    radius=300,
                    get_color='[51, 255, 207, 0]',
                    elevation_scale=4,
                    elevation_range=[0, 1000],
                    pickable=True,
                    extruded=True,
                ),
            ]
        ))

    def new(df, hour_selected):

        return df[df['DateTime'] == hour_selected]

    # LAYING OUT THE TOP SECTION OF THE APP
    row1_1, row1_2 = st.columns((2, 3))

    with row1_1:
        st.title("Data")
        st.subheader('Nb of locations by hour')
        df_time = df_hour.drop(columns=['lon', 'lat'])
        df_time.hist()
        df_time.hist()
        plt.rcParams["figure.figsize"] = (80, 20)
        plt.show()
        st.pyplot()
        hour_selected = st.slider("Select hour of pickup", 0, 23)

    with row1_2:

        st.write("##")
        st.write("##")
        st.write("##")
        st.write("##")
        st.write("##")

        st.markdown("<p style='text-align: center;font-weight: bold; color: white;'>Snapchat has probably used a similar survey system as the one I show you today combining Dates and Locations</p>",
                    unsafe_allow_html=True)
    # LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS
    row2_1, row2_2, row2_3, row2_4 = st.columns((2, 1, 1, 1))

    # SETTING THE ZOOM LOCATIONS FOR THE AIRPORTS
    loc1 = [50.3946, 2.024]
    loc2 = [45.624,  5.224]
    loc3 = [37.970681, 23.736414]
    zoom_level = 11
    midpoint = [48.8134, 2.330]

    with row2_1:

        st.write("**All my locations by frequency  \nfrom %i:00 and %i:00**" %
                 (hour_selected, (hour_selected + 1) % 24))
        map(new(df, hour_selected),
            midpoint[0], midpoint[1], 11)

    with row2_2:
        st.markdown(
            '''<p style='text-align: center; color: red;'>Huby-Saint-Leu <br />(hacking location)</p>''', unsafe_allow_html=True)
        map(df, loc1[0], loc1[1], zoom_level)

    with row2_3:
        st.markdown(
            '''<p style='text-align: center; color: red;'>L'Isle-d'Abeau <br /> (hacking location)</p>''', unsafe_allow_html=True)
        map(df, loc2[0], loc2[1], zoom_level)

    with row2_4:

        st.markdown(
            '''<p style='text-align: center; color: lightblue;'>Athens <br /> (vacation location)</p>''', unsafe_allow_html=True)

        map(df, loc3[0], loc3[1], zoom_level)
