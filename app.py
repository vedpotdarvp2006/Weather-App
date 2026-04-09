import streamlit as st      # For creating web app UI
import requests             # For fetching data from OpenWeatherMap API

# ============================================================
# 🔑 API CONFIGURATION
# ============================================================
API_KEY = "96c0c6f573d41560b89c2d2fa86b936d"                  # Replace with your OpenWeatherMap API key
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"  # API endpoint URL

# ============================================================
# 🎨 CUSTOM CSS STYLING
# ============================================================
st.markdown("""
<style>
/* 🌈 App background gradient */
.stApp {
    background: linear-gradient(to right, mediumturquoise, lightsteelblue);
}

/* 🟢 Get Weather button styling */
div.stButton > button {
    background-color: black;
    color: white;
    border-radius: 10px;                 
    height: 3em;               
    width: 100%;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# 🏷️ APP TITLE
# ============================================================
st.markdown(
    "<h1 style='text-align: center;'>🌦️ Weather Information Fetcher</h1>",
    unsafe_allow_html=True)
# ============================================================
# 📥 CITY NAME INPUT LABEL WITH CUSTOM FONT SIZE
# ============================================================
#st.markdown("<p style='font-size: 18px;'>Enter City Name</p>", unsafe_allow_html=True)
city = st.text_input("", placeholder="Enter City Name")              # Label hidden, shown via markdown above
# ============================================================
# 🔘 FETCH WEATHER BUTTON
# ============================================================
if st.button("Get Weather"):

    # ⚠️ Validate: Check if city input is empty
    if city == "":
        st.warning("Please enter a city name!")

    else:
        # -------------------------------------------------------
        # 📡 API REQUEST SETUP
        # -------------------------------------------------------
        params = {
            "q": city,           # City name entered by user
            "appid": API_KEY,    # Your API key for authentication
            "units": "metric"    # Use "imperial" for Fahrenheit, "metric" for Celsius
        }

        # 🌐 Send GET request to OpenWeatherMap API
        response = requests.get(BASE_URL, params=params)

        # 📦 Parse JSON response from API
        data = response.json()

        # -------------------------------------------------------
        # ❌ ERROR HANDLING: City Not Found
        # -------------------------------------------------------
        if data["cod"] != 200:
            st.error("City not found! Please check the city name and try again.")

        else:
            # ---------------------------------------------------
            # 📊 EXTRACT WEATHER DATA FROM API RESPONSE
            # ---------------------------------------------------
            temp         = data["main"]["temp"]                  # Temperature in °C
            humidity     = data["main"]["humidity"]              # Humidity in %
            wind         = data["wind"]["speed"]                 # Wind speed in m/s
            weather_desc = data["weather"][0]["description"]     # Weather description
            country      = data["sys"]["country"]                # Country code
            # ---------------------------------------------------
            # 🌤️ WEATHER CONDITION: EMOJI + SMART MESSAGE
            # ---------------------------------------------------
            if "clear" in weather_desc:
                emoji     = "☀️"
                smart_msg = "🌤️ <b>Clear sky, enjoy your day!</b>"

            elif "cloud" in weather_desc:
                emoji     = "☁️"
                smart_msg = "☁️ <b>It's cloudy today.</b>"

            elif "rain" in weather_desc:
                emoji     = "🌧️"
                smart_msg = "🌧️ <b>Don't forget your umbrella!</b>"

            elif "storm" in weather_desc:
                emoji     = "⛈️"
                smart_msg = "⛈️ <b>Stay safe, storm ahead!</b>"

            else:
                # Default case for any other weather condition
                emoji     = "🌍"
                smart_msg = "🌍 <b>Stay prepared for the weather!</b>"

            # ---------------------------------------------------
            # 🃏 WEATHER CARD UI
            # ---------------------------------------------------
            st.markdown(f"""
            <div style="
                background-color: white;
                padding: 25px;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
                margin-top: 10px;
            ">
                <h1>{emoji}</h1>
                <h2>Weather in {city.capitalize()}, {country}</h2>
                <h1>{temp}°C</h1>
                <p><b>Condition:</b> {weather_desc.capitalize()}</p>
                <p>💧 Humidity: {humidity}%</p>
                <p>🌬️ Wind Speed: {wind} m/s</p>
                <hr style="border: 1px solid darkgray; margin: 15px 0;">
                <p style="font-size: 20px; color: black;">{smart_msg}</p>
            </div>
            """, unsafe_allow_html=True)

            # ---------------------------------------------------
            # 📌 FOOTER
            # ---------------------------------------------------
            st.markdown("---")
            st.caption("Developed by Ved Potdar | Real-time Weather App 🌍")