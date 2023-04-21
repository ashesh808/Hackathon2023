import requests
import json
import math

base_url = "https://developer.nrel.gov/"
lat = "40"
lon = "-105"
lat = "45.465135"# St. Cloud MN
lon = "-94.251555"#St. Cloud MN

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
# DNI is the Direct Normal Irradiance in Kwh/M^2/day
# Area is the surface area of the solar panel in m^2
# Efficiency is the efficiency of the solar panel (usually given as a percentage)
# Time is the time duration for which the solar panel is exposed to the sun in hours

annual_Energy = annual_avg_dni * 0.5471 * 0.22 * 365 * 0.75 # the *0.75 could be omitted. I'm not sure.

grid_electricity_cost = 0.1409 #Cents per Kwh
cost_of_system = 124.99+439.99 #Cost of total installation
annual_cost_savings = round(annual_Energy*grid_electricity_cost,2)
payback_years = round(cost_of_system/annual_cost_savings,2)

#print(annual_avg_dni)

print("The average annual solar energy generated for latitude: " + lat + " and longitude: " + lon + " is " + str(annual_Energy) + " kWh")

print("The cost savings from this system could be as much as $" + str(annual_cost_savings) + " Per Year" )

print("The payback period could be as little as " + str(payback_years) + " years.")

