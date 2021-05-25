import streamlit as st
import pandas as pd
import time
import datetime
import geopy
from geopy.geocoders import Nominatim
from streamlit_folium import folium_static
import folium
from PIL import Image
import random


def get_latlo(address):
    geolocator = Nominatim(user_agent="busy")
    location = geolocator.geocode(address)
    loc_stats = (location.latitude, location.longitude)
    return loc_stats

Rosenthaler_lat = 52.5313683
Rosenthaler_lon = 13.4

img_business_lunch = Image.open("data/business_lunch_logo.jpg")
st.sidebar.image(img_business_lunch, width=120)

restaurant_df = pd.read_csv('data/restaurants.csv', sep=',')

function = st.sidebar.radio(
    "What do your want to do?",
    ('Home', 'Get Recommendation', 'Add Restaurant', 'Add a Dish', 'Rate a restaurant', 'Show Data'))
st.sidebar.write("----------------")
#### Home config ############################################################################

if function == 'Home':
    st.success("This service only works for the area around Rosenthaler Platz, Berlin... yet ;)")
    st.header("Thanks for choosing Business Lunch\n")
    st.write("This service will help you to decide to where you should have lunch with your colleagues, because yet again it is difficult to satisfy everybody. Go to 'get recommendation' to get a suggestions that fulfills your criteria. The result will be a random selection of a restaurant from the existing database. If you are unhappy with the database, feel free to extend it at 'add a restaurant'")

    n = folium.Map(location=[Rosenthaler_lat, Rosenthaler_lon], zoom_start=16, tiles="openstreetmap")
    #folium.Rectangle(bounds=points, color='#5dbb63', fill=True, fill_color='5dbb63', fill_opacity=0.1).add_to(m)
    for index, row in restaurant_df.iterrows():
        pin = row.name
        lat1, lon1 = get_latlo(row.street+' '+str(row.number)+', '+str(row.zip_code)+', Berlin')
        folium.Marker([lat1, lon1], popup=row.name, tooltip=pin).add_to(n)
    folium_static(n)
    st.write(restaurant_df)

#### Get Recommendation ############################################################################
elif function == 'Get Recommendation':
    choice_df = restaurant_df
    st.subheader('Let me help you to find a business lunch around Rosenthaler Platz.')
    st.sidebar.write("\n Let's set some preferences.\n")
    diet = st.sidebar.radio(
        "Which options do you need?",
        ("All carnivores 🦖", "Vegetarians present 🌯", "Vegans present 🥗")
    )
    fancy = st.sidebar.radio(
        "How fancy should it be?",
        ("Give me sth quick and cheap 💶", "Some decent food 💶💶", "A bit nicer please 💶💶💶"))
    recommend = st.sidebar.button("Give me the recommendation")
    
    if diet == "Vegetarians present 🌯":
        veggi_rec = 1
        vegan_rec = 0
    elif diet =="Vegans present 🥗":
        veggi_rec = 1
        vegan_rec = 1
    else:
        veggi_rec = 0
        vegan_rec = 0
        
    if fancy == "Give me sth quick and cheap 💶":
        choice_df = choice_df[choice_df.price == 1]
    elif fancy == "Some decent food 💶💶":
        choice_df = choice_df[choice_df.price == 2]
    else:
        choice_df = choice_df[choice_df.price == 3]
    
    if recommend:
        choice_df = choice_df.reset_index()
        random_num = random.choice(choice_df.index.to_list())
        st.subheader("... and here is your suggestions 🍽")
        st.write(choice_df.name[random_num])
        st.write(choice_df.street[random_num], choice_df.number[random_num])
        st.write(choice_df.type[random_num]+" restaurant")
        
        m = folium.Map(location=[Rosenthaler_lat, Rosenthaler_lon], zoom_start=16, tiles="openstreetmap")
        pin2 = "Restaurant Location"
        lat1, lon1 = get_latlo(choice_df.street[random_num]+' '+str(choice_df.number[random_num])+', '+str(choice_df.zip_code[random_num])+', Berlin')
        folium.Marker([lat1, lon1], popup=choice_df.name[random_num], tooltip=pin2).add_to(m)
        folium_static(m)
        st.write(choice_df.head(5)[['name','street','number','type']])

   
    
#### Ad Restaurant ############################################################################    
elif function == 'Add Restaurant':
    st.subheader("Which restaurant do you want to add?")
    name_input = st.text_input("Name of Restaurant", "Berlin Burrito Company")
    street_input = st.text_input("Name of Street", "Kastanienallee")
    number_input = st.number_input("House number", 0, 300, 59, 1)
    zip_input = st.number_input("zip code", 00000, 99999, 10119, 1)
    type_input = st.text_input("Restaurant type", "mexican")
    diet = st.radio(
        "What options do they serve?",
        ("Meat and fish only", "Vegetarian", "Vegan")
    )
    fancy = st.radio(
        "How fancy is it??",
        ("It is sth quick and cheap 💶", "It has decent food 💶💶", "It is a bit nicer 💶💶💶"))
    if diet == "Vegetarian":
        vegetarian = 1
        vegan = 0
    elif diet == "Vegan":
        vegetarian = 1
        vegan = 1
    else:
        vegetarian = 0
        vegan = 0
        
    if fancy == "It is sth quick and cheap 💶":
        price = 1
    elif fancy == "It has decent food 💶💶":
        price = 2
    elif fancy == "It is a bit nicer 💶💶💶":
        price = 3
    
    opening = st.time_input("When does this restaurant open?", value=datetime.datetime(2021, 10, 6, 12, 00, 20))
    closing = st.time_input("When does this restaurant close?", value=datetime.datetime(2021, 10, 6, 21, 00, 20))
    id = int(restaurant_df.restaurant_id[len(restaurant_df)-1]) +1
    if (street_input in restaurant_df.street.to_list()) & (number_input in restaurant_df.number.to_list()):
        st.sidebar.warning("This restaurant is already in the database")
    else:    
        confirm_rest = st.sidebar.button("Confirm")

        if confirm_rest:
            new_line_df = pd.DataFrame([[id,name_input,street_input,number_input,zip_input,type_input,opening,closing,vegetarian,vegan, price]],columns = restaurant_df.columns.to_list())
            restaurant_df = pd.concat([restaurant_df, new_line_df])
            restaurant_df.to_csv("data/restaurants.csv", index=False)
            
#### Add Dish ######################################################################
elif function == 'Add a Dish':
    st.warning("This Feature does not work yet")


#### Rate a Restaurant ######################################################################
elif function == 'Rate a restaurant':
    st.warning("This Feature does not work yet")

#### Show Data ######################################################################
elif function == 'Show Data':
    st.warning("This Feature does not work yet")
    st.write(restaurant_df)
