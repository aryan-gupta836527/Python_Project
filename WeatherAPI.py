import requests
import time
from api import api_request
class WeatherAPI:
    def __init__(self,city):
        self.url_search = "https://geocoding-api.open-meteo.com/v1/search"
        self.url_forecast = "https://api.open-meteo.com/v1/forecast"
        self.city = city
        self.params_search = {"name":self.city,"count":1}
        self.latitude= None
        self.longitude= None
        self.weather_data = None
        self.cache = {}
        self.get_location()
        self.get_weather_data()
    def get_weather_data(self):
        params_forecast = {"latitude":self.latitude,"longitude":self.longitude,"current":"temperature_2m,wind_speed_10m,weather_code","daily":"temperature_2m_max,temperature_2m_min"}
        self.weather_data = api_request("GET",self.url_forecast,params=params_forecast)
        return self.weather_data
    def get_location(self):
        data = api_request("GET",self.url_search,params=self.params_search)
        if not data.get("results"):
            raise ValueError(f"City '{self.city}' not found.")
        self.latitude = data["results"][0]["latitude"]
        self.longitude = data["results"][0]["longitude"]
    def get_weather(self):
        data = self.weather_data
        return {"temperature": data["current"]["temperature_2m"],"wind_speed": data["current"]["wind_speed_10m"]}
    def get_forecast(self):
        data = self.weather_data
        forecast = []
        for i in range(3):
            forecast.append({"date":data["daily"]["time"][i],
                             "temperature_max":data["daily"]["temperature_2m_max"][i],
                             "temperature_min":data["daily"]["temperature_2m_min"][i]})
        return forecast
    def get_weather_description(self):
        data = self.weather_data
        weather_code=data["current"]["weather_code"]
        if weather_code == 0:
            weather = "Clear sky"
        elif 1 <= weather_code <= 3:
            weather = "Cloudy"
        elif 51 <= weather_code <= 67:
            weather = "Rain"
        elif 71 <= weather_code <= 77:
            weather = "Snow"
        elif weather_code >= 95:
            weather = "Thunderstorm"
        else:
            weather = "Unknown"
        return weather
    def get_cached_weather_data(self):
        if self.city in self.cache and time.time() - self.cache[self.city]["time"] < 600:
            return self.cache[self.city]
        else:
            data = self.get_weather()
            forecast = self.get_forecast()
            weather_description = self.get_weather_description()
            self.cache[self.city] = {"data":data,"data_forecast":forecast,"weather_description":weather_description,"time":time.time()}
            return self.cache[self.city]
city=input("City: ")
API=WeatherAPI(city)
try:
    data = API.get_cached_weather_data()
    print(data)
    print(f"""================================
       WEATHER REPORT
================================

    Location: {city}

    Current Weather: {data["data"]["temperature"]} °C
    Wind Speed: {data["data"]["wind_speed"]} km/h
    Condition: {data["weather_description"]}

        3-Day Forecast
------------------------------------
    Date        Min       Max""")

    for day in data["data_forecast"]:
        print(
            f"{day['date']}    "
            f"{day['temperature_min']} °C    "
            f"{day['temperature_max']} °C"
        )
except requests.exceptions.RequestException as e:
    print(e)
except ValueError as e:
    print(e)