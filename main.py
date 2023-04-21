import requests
import json

base_url = "https://developer.nrel.gov/"
lat = "40"
lon = "-105"
response = requests.get(base_url + "api/solar/solar_resource/v1.json?api_key=DEMO_KEY&lat=" + lat + "&lon=" + lon)


def get_request():
    if response.status_code == 200:
        jsonData = response.json()
        #print(jsonData)
        # Do something with the data
    else:
        print(f"Error: {response.status_code}")
    data = json.loads(json.dumps(jsonData))
    return data

data = get_request()
annual_avg_dni = float(data['outputs']['avg_dni']['annual'])


# Energy = DNI x Area x Efficiency x Time
# Where:
# DNI is the Direct Normal Irradiance in W/m^2
# Area is the surface area of the solar panel in m^2
# Efficiency is the efficiency of the solar panel (usually given as a percentage)
# Time is the time duration for which the solar panel is exposed to the sun in hours

annual_Energy = annual_avg_dni * 1 * 0.2 * 6

print("The average annual solar energy generated for latitude: " + lat + " and longitude: " + lon + " is " + str(annual_Energy) + " kWh")
