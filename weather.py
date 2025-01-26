import streamlit as st
import requests
from datetime import datetime
# Streamlit Title
st.title("🌤 Weather App")

# Sidebar for input
st.sidebar.title("Options")
city_input = st.sidebar.text_area("Enter city names (comma separated)")

api_key = "37bb575a48dd55b8171a35e9a2386bca"

@st.cache_data(ttl=600)  # Cache data for 10 minutes
def get_weather(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Multi-city Weather
if city_input:
    cities = [city.strip() for city in city_input.split(',')]
    for city in cities:
        weather_data = get_weather(city)
        if weather_data:
            st.subheader(f"Weather in {city}")
            
            # Weather details
            st.write(f"**Weather:** {weather_data['weather'][0]['description']}")
            st.write(f"**Temperature:** {weather_data['main']['temp']} °C")
            st.write(f"**Humidity:** {weather_data['main']['humidity']}%")
            st.write(f"**Wind Speed:** {weather_data['wind']['speed']} m/s")
            st.write(f"**Pressure:** {weather_data['main']['pressure']} hPa")
            
            # Sunrise and Sunset Time
            sunrise = datetime.utcfromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M:%S')
            sunset = datetime.utcfromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M:%S')
            st.write(f"**Sunrise:** {sunrise} UTC")
            st.write(f"**Sunset:** {sunset} UTC")

            # Display Weather Icon
            icon_url = f"http://openweathermap.org/img/wn/{weather_data['weather'][0]['icon']}@2x.png"
            st.image(icon_url, caption="Weather Icon")

        else:
            st.error(f"Could not fetch data for {city}. Please check the city name.")
