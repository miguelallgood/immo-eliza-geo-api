import os
import sys
import streamlit as st
import requests
import googlemaps
from googlemaps.exceptions import ApiError
from predict import Item
from dotenv import load_dotenv

# Add parent directory of predict.py to Python path
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

# Load environment variables from .env file
load_dotenv()
# Access environment variables
api_key = os.getenv('API_KEY')

# Initialize Google Maps client with your API key
gmaps = googlemaps.Client(key = api_key)

def get_coordinates(address):
    try:
        # Geocode the address to retrieve latitude and longitude
        geocode_result = gmaps.geocode(address)

        if geocode_result:
            # Extract latitude and longitude from the geocode result
            location = geocode_result[0]['geometry']['location']
            latitude = location['lat']
            longitude = location['lng']
            return latitude, longitude
        else:
            st.error("No geocode result found for the address.")
            return None, None

    except ApiError as e:
        st.error(f"Error occurred: {e}")
        return None, None

st.title('Apartment for sale')

st.write('Enter the full address below:')
street_name = st.text_input('Street Name')
property_number = st.text_input('Property Number')
postcode = st.text_input('Postcode')

latitude = None
longitude = None

# Construct full address
address = f'{property_number} {street_name}, {postcode}'
# Get latitude and longitude using Google Maps Geocoding API
latitude, longitude = get_coordinates(address)

st.write('Enter the features below:')
number_rooms = st.number_input('Number of Rooms', min_value=0)
living_area = st.number_input('Living Area (m²)', step=20)
garden_area = st.number_input('Garden Area (m²)', step=10)
number_facades = st.number_input('Number of Facades', min_value=0)

if st.button('Predict Price'):
    latitude, longitude = get_coordinates(address)
    # Check if latitude and longitude are available
    if latitude is not None and longitude is not None:
        # Create an Item object with the entered features
        item = Item(
            number_rooms=number_rooms,
            living_area=living_area,
            garden_area=garden_area,
            number_facades=number_facades,
            Longitude=longitude,
            Latitude=latitude
        )

        # Make a POST request to the FastAPI backend for price prediction
        response = requests.post('https://immo-eliza-fastapi.onrender.com', json=item.dict())

        if response.status_code == 200:
            prediction = response.json()['prediction']
            formatted_prediction = f'{prediction:,.2f} €'  # Format prediction with 2 decimals and euro sign
            st.success(f'Predicted Price: {formatted_prediction}')
        else:
            st.error('Price prediction failed. Please try again.')
    else:
        st.error('Latitude and longitude are not available. Please get latitude and longitude first.')
