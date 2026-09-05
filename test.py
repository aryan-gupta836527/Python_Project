import requests
import time
def api_request(method, url, headers=None, params=None,json=None,data=None,timeout=10,max_retries=3):
    attempts=0
    while True:
        response=requests.request(method, url, headers=headers, params=params, json=json, data=data, timeout=timeout)
        if response.status_code==429:
            if attempts >= max_retries:
                raise requests.exceptions.RequestException("Max retries exceeded")
            retry_after=response.headers.get("retry-after")
            if retry_after:
                wait=int(retry_after)
            else:
                wait=2**attempts
            print(f"Retrying in {wait} seconds...")
            time.sleep(wait)
            attempts+=1
            continue
        response.raise_for_status()
        return response.json()
def get_weather(city):
    url_search="https://geocoding-api.open-meteo.com/v1/search"
    url_forecast="https://api.open-meteo.com/v1/forecast"
    name_city=city
    params_search={"name":name_city,"count":1}
    data_search=api_request('GET',url_search,params=params_search)
    if not data_search.get("results"):
        raise ValueError("City not found")
    params_forecast={"latitude":data_search["results"][0]["latitude"],"longitude":data_search["results"][0]["longitude"],"current":"temperature_2m,wind_speed_10m,weather_code",
                     "daily":"temperature_2m_max,temperature_2m_min"}
    data_forecast=api_request('GET',url_forecast,params=params_forecast)
    weather_code = data_forecast["current"]["weather_code"]
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
    forecast = []
    for i in range(3):
        forecast.append({
            "date": data_forecast["daily"]["time"][i],
            "max": data_forecast["daily"]["temperature_2m_max"][i],
            "min": data_forecast["daily"]["temperature_2m_min"][i]
        })
    return {"city":name_city,"temperature":data_forecast["current"]["temperature_2m"],"wind_speed":data_forecast["current"]["wind_speed_10m"],"weather":weather,
            "forecast":forecast}
def send_alert(data):
    url_alert = "https://api.example.com/alerts"
    req_body={"city":data["city"],"temperature":data["temperature"],"weather":data["weather"],"message": "High temperature alert"}
    return api_request('POST', url_alert, json=req_body)
city=input("City: ")
try:
    data=get_weather(city)
    print(f"""\t================================
           WEATHER REPORT
\t================================
    
    Location: {city}
    
    Current Weather: {data['temperature']} °C
    Wind Speed: {data['wind_speed']} km/h
    Condition: {data['weather']}
    
    3-Day Forecast
    --------------------------------
    Date            Min        Max""")

    for day in data["forecast"]:
        print(
            f"{day['date']}    "
            f"{day['min']} °C    "
            f"{day['max']} °C"
        )
    if data["temperature"]>30:
        alert_response=send_alert(data)
        print("Alert sent",alert_response)
except requests.exceptions.RequestException as e:
    print(e)
except ValueError as e:
    print(e)