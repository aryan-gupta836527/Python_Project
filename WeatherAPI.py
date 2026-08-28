import requests
from api import api_request
class WeatherAPI:
    def __init__(self,city):
        self.url_search = "https://geocoding-api.open-meteo.com/v1/search"
        self.url_forecast = "https://api.open-meteo.com/v1/forecast"
        self.city = city
        self.params_search = {"name":self.city,"count":1}
        self.latitude= None
        self.longitude= None
    def get_location(self):
        data = api_request("GET",self.url_search,params=self.params_search)
        self.latitude = data["results"][0]["latitude"]
        self.longitude = data["results"][0]["longitude"]
    def get_weather(self):
        params_forecast = {"latitude":self.latitude,"longitude":self.longitude,"current":"temperature_2m,wind_speed_10m"}
        data = api_request("GET",self.url_forecast,params=params_forecast)
        return {"temperature":data["current"]["temperature_2m"],"wind_speed":data["current"]["wind_speed_10m"]}
    def get_forecast(self):
        params_forecast = {"latitude":self.latitude,"longitude":self.longitude,"daily":"temperature_2m_max,temperature_2m_min"}
        data = api_request("GET",self.url_forecast,params=params_forecast)
        forecast=[]
        for i in range(3):
            forecast.append({"date":data["daily"]["time"][i],
                             "temperature_max":data["daily"]["temperature_2m_max"][i],
                             "temperature_min":data["daily"]["temperature_2m_min"][i]})
        return forecast
    def get_weather_code(self):
        params_forecast = {"latitude":self.latitude,"longitude":self.longitude,"current":"weather_code"}
        data = api_request("GET",self.url_forecast,params=params_forecast)
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
city=input("City: ")
API=WeatherAPI(city)
API.get_location()
try:
    data = API.get_weather()
    data_forecast = API.get_forecast()
    weather = API.get_weather_code()
    print(f"""================================
       WEATHER REPORT
================================

    Location: {city}

    Current Weather: {data['temperature']} °C
    Wind Speed: {data['wind_speed']} km/h
    Condition: {weather}

        3-Day Forecast
------------------------------------
    Date        Min       Max""")

    for day in data_forecast:
        print(
            f"{day['date']}    "
            f"{day['temperature_min']} °C    "
            f"{day['temperature_max']} °C"
        )
except requests.exceptions.RequestException as e:
    print(e)
except ValueError as e:
    print(e)
