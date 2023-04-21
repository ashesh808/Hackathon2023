import requests
import matplotlib.pyplot as plt
import json

base_url = "https://developer.nrel.gov/"
lat = "40"
lon = "-105"
addr = "56387"
response = requests.get(base_url + "api/solar/solar_resource/v1.json?api_key=DEMO_KEY&address=" + addr)


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

annual_Energy = annual_avg_dni * 1 * 0.2

print("The average annual solar energy generated for zip code " + addr + " is " + str(annual_Energy) + " kWh")

monthly_dni = data["outputs"]["avg_dni"]["monthly"]
monthly_ghi = data["outputs"]["avg_ghi"]["monthly"]

figures, axes = plt.subplots(2,2)
axes[0][0].bar(monthly_dni.keys(), monthly_dni.values())
axes[0][1].bar(monthly_ghi.keys(), monthly_ghi.values())
plt.show()
