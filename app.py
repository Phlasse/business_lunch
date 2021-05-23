import streamlit as st
import pandas as pd
import time
import datetime
import requests
import geopy
from geopy.geocoders import Nominatim
from streamlit_folium import folium_static
import folium
from PIL import Image

def get_latlo(address):
    geolocator = Nominatim(user_agent="busy")
    location = geolocator.geocode(address)
    loc_stats = (location.latitude, location.longitude)
    return loc_stats

restaurant_df = pd.read_csv('data/restaurants.csv', sep=';')
st.header("Welcome to Business Lunch")

function = st.sidebar.radio(
    "What do your want to do?",
    ('Home', 'Get Recommendation', 'Add Restaurant', 'Add a Dish'))
st.sidebar.write("\n----------------\n")
#### Home config ####

if function == 'Home':
    st.write("Thanks for choosing Business Lunch")

#### Get Recommendation #####
elif function == 'Get Recommendation':
    Rosenthaler_lat = 52.5313683
    Rosenthaler_lon = 13.4
    st.subheader('Let me help you to find a business lunch around Rosenthaler Platz.')
    st.sidebar.write("\n Let's set some preferences.\n")
    diet = st.sidebar.radio(
        "Which options do you need?",
        ("All carnivores 🦖", "Vegetarians present 🌯", "Vegans present 🥗")
    )
    fancy = st.sidebar.radio(
        "How fancy should it be?",
        ("Give me sth quick and cheap [<7 💶]", "Some decent food [<12 💶]", "A bit nicer please [10+ 💶]"))
    recommend = st.sidebar.button("Give me the recommendation")
    if recommend:
        st.write(restaurant_df.head(5)[['name','street','number','type']])
        m = folium.Map(location=[Rosenthaler_lat, Rosenthaler_lon], zoom_start=16, tiles="openstreetmap")
    #folium.Rectangle(bounds=points, color='#5dbb63', fill=True, fill_color='5dbb63', fill_opacity=0.1).add_to(m)
        pin = "Restaurant Location"
        folium.Marker([restaurant_df.lat[0], restaurant_df.lon[0]], popup=restaurant_df.name[0], tooltip=pin).add_to(m)
        pin2 = "Restaurant Location"
        lat1, lon1 = get_latlo("Kastanienallee, 59, 10119, Berlin")
        folium.Marker([lat1, lon1], popup=restaurant_df.name[0], tooltip=pin2).add_to(m)
        folium_static(m)
   
    
#### Ad Restaurant ####    
elif function == 'Add Restaurant':
    st.subheader("Which restaurant do you want to open?")
    name_input = st.text_input("Name of Restaurant")
    street_input = st.text_input("Name of Street")
    number_input = st.number_input("House number")
    zip_input = st.number_input("zip code")
    type_input = st.text_input("Restaurant type")
    confirm_rest = st.button("Confirm")
    if confirm_rest:
        add_rest=False
    cancel_rest_add = st.button("cancel adding")
    if cancel_rest_add:
        add_rest=False
        
#### Add Dish ####
elif function == 'Add a Dish':
    st.write("Which dish do you want to add?")

    name_input = st.text_input("Name of Restaurant")
    street_input = st.text_input("Name of Street")
    number_input = st.number_input("House number")
    zip_input = st.number_input("zip code")
    type_input = st.text_input("Restaurant type")
    confirm_rest = st.button("Confirm")
    if confirm_rest:
        add_rest=False
    cancel_rest_add = st.button("cancel adding")
    if cancel_rest_add:
        add_rest=False
