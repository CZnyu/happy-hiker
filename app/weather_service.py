# app/weather_service.py

import os
import csv
import json
from pprint import pprint

import requests
from dotenv import load_dotenv

from app import APP_ENV

csv_filepath = os.path.join(os.path.dirname(__file__), "Trail Park Database - Parks.csv")

with open(csv_filepath, "r") as csv_file:
    parks = []
    reader = csv.DictReader(csv_file)
    for row in reader:
        parks.append(row)

print("-----------------------------")
print("Hey Happy Hiker!")
print("-----------------------------")
print("Please select from the list below: ")
print("-----------------------------")

original = []
for z in parks:
    print(z["park"])

print("-----------------------------")

destination = []
while True:
    park_id = input("Please Input Your Park to Start Your Adventure: ")

    if [p for p in parks if str(p["park"]) == park_id]:
        destination.append(park_id)
        break
    else:
        print("We don't play there! Please Re-Enter.")

for park_id in destination:
    matching_locations = [i for i in parks if str(i["park"]) == str(park_id)]
    matching_location = matching_locations[0]
    for i in matching_locations:
        park_zip_code = i["zipcode"]

load_dotenv()

OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
PARK_ZIP = ("park_zip_code")
COUNTRY_CODE = os.getenv("COUNTRY_CODE", default="US")

def human_friendly_temp(my_temperature_f):
    """Rounds a decimal fahrenheit temperature to the nearest whole degree, adds degree symbol"""
    degree_sign = u"\N{DEGREE SIGN}"
    return f"{round(my_temperature_f)} {degree_sign}F"

def get_hourly_forecasts(zip_code=PARK_ZIP, country_code=COUNTRY_CODE):
    # see: https://openweathermap.org/current
    request_url = f"https://api.openweathermap.org/data/2.5/forecast?zip={zip_code},{country_code}&units=imperial&appid={OPEN_WEATHER_API_KEY}"
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)
    #print(parsed_response.keys()) #> dict_keys(['cod', 'message', 'cnt', 'list', 'city'])
    result = {
        "city_name": parsed_response["city"]["name"],
        "hourly_forecasts": []
    }
    for forecast in parsed_response["list"][0:9]:
        #print(forecast.keys()) #> dict_keys(['dt', 'main', 'weather', 'clouds', 'wind', 'sys', 'dt_txt'])
        result["hourly_forecasts"].append({
            "timestamp": forecast["dt_txt"],
            "temp": human_friendly_temp(forecast["main"]["feels_like"]),
            "conditions": forecast["weather"][0]["description"]
        })
    return result

if __name__ == "__main__":

    if APP_ENV == "development":
        #park_name = input("HEY HAPPY HIKER! PLEASE SELECT YOUR PARK (e.g. Bear Mountain State Park): ")

        results = get_hourly_forecasts(zip_code=zip_code) # invoke with custom params
    else:
        results = get_hourly_forecasts() # invoke with default params

    print("-----------------")
    print(f"TODAY'S WEATHER FORECAST FOR {results['city_name'].upper()}...")
    print("-----------------")

    for hourly in results["hourly_forecasts"]:
        print(hourly["timestamp"], "|", hourly["temp"], "|", hourly["conditions"])
