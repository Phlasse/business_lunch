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
    print(location)
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
        choice_df = restaurant_df
        st.write(choice_df.head(5)[['name','street','number','type']])
        m = folium.Map(location=[Rosenthaler_lat, Rosenthaler_lon], zoom_start=16, tiles="openstreetmap")
    #folium.Rectangle(bounds=points, color='#5dbb63', fill=True, fill_color='5dbb63', fill_opacity=0.1).add_to(m)
        pin2 = "Restaurant Location"
        lat1, lon1 = get_latlo(choice_df.street[0]+' '+str(choice_df.number[0])+', '+str(choice_df.zip_code[0])+', Berlin')
        folium.Marker([lat1, lon1], popup=choice_df.name[0], tooltip=pin2).add_to(m)
        folium_static(m)
   
    
#### Ad Restaurant ####    
elif function == 'Add Restaurant':
    st.subheader("Which restaurant do you want to add?")
    name_input = st.text_input("Name of Restaurant")
    street_input = st.text_input("Name of Street")
    number_input = st.number_input("House number", 0, 300, 1, 1)
    zip_input = st.number_input("zip code", 00000, 99999, 10115, 1)
    type_input = st.text_input("Restaurant type")
    diet = st.radio(
        "What options do they serve?",
        ("Meat and fish only", "Vegetarian", "Vegan")
    )
    fancy = st.radio(
        "How fancy is it??",
        ("It is sth quick and cheap [<7 💶]", "It has decent food [<12 💶]", "It is a bit nicer. [10+ 💶]"))
    if diet == "Vegetarian":
        vegetarian = 1
        vegan = 0
    elif diet == "Vegan":
        vegetarian = 1
        vegan = 1
    else:
        vegetarian = 0
        vegan = 0
    confirm_rest = st.sidebar.button("Confirm")
    if confirm_rest:
        new_line_df = pd.DataFrame([[0,name_input,street_input,number_input,zip_input,type_input,0,0,vegetarian,vegan]],columns = restaurant_df.columns.to_list())
        st.write(new_line_df)        
        
#### Add Dish ####
elif function == 'Add a Dish':
    st.write("Which dish do you want to add?")

    name_input = st.text_input("Name of Restaurant")
    street_input = st.text_input("Name of Street")
    number_input = st.number_input("House number")
    zip_input = st.number_input("zip code")
    type_input = st.text_input("Restaurant type")
    confirm_rest = st.sidebar.button("Confirm")
    if confirm_rest:
        add_rest=False
    cancel_rest_add = st.sidebar.button("cancel adding")
    if cancel_rest_add:
        add_rest=False
