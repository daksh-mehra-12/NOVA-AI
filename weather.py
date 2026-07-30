import os
import urllib.parse
import requests
from logger import log_command, log_error
from voice import speak

def getWeather(city):
    if not city:
        speak("Which city's weather would you like to check?")
        return

    api_key = os.getenv("OPENWEATHER_API_KEY", "YOUR_OPENWEATHER_API_KEY")

    if api_key != "YOUR_OPENWEATHER_API_KEY":
        url = f"https://api.openweathermap.org/data/2.5/weather?q={urllib.parse.quote(city)}&appid={api_key}&units=metric"
        try:
            res = requests.get(url, timeout=5)
            data = res.json()
            if res.status_code == 200 and str(data.get("cod")) == "200":
                temp = data["main"]["temp"]
                desc = data["weather"][0]["description"]
                humidity = data["main"]["humidity"]
                msg = f"The temperature in {city} is {temp} degrees Celsius with {desc}. Humidity is {humidity} percent."
                speak(msg)
                log_command(f"weather in {city}", msg)
                return
        except Exception as e:
            log_error(f"OpenWeather API error for {city}", e)

    try:
        url = f"https://wttr.in/{urllib.parse.quote(city)}?format=j1"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            current = data["current_condition"][0]
            temp = current["temp_C"]
            desc = current["weatherDesc"][0]["value"]
            humidity = current["humidity"]
            wind_kmh = current["windspeedKmph"]

            msg = f"In {city}, the temperature is {temp} degrees Celsius with {desc}. Humidity is {humidity} percent and wind speed is {wind_kmh} kilometers per hour."
            speak(msg)
            log_command(f"weather in {city}", msg)
            return
    except Exception as e:
        log_error(f"wttr.in weather error for {city}", e)

    speak(f"Unable to fetch weather details for {city}.")
