import requests
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
import json
import math

base_url = "https://developer.nrel.gov/"
lat = "40"
lon = "-105"
lat = "45.465135"# St. Cloud MN
lon = "-94.251555"#St. Cloud MN

addr = "56301" #zip code for requesting solar data that way
response = requests.get(base_url + "api/solar/solar_resource/v1.json?api_key=DEMO_KEY&address=" + addr)

#Requesting solar data via latitude and longitude
#response = requests.get(base_url + "api/solar/solar_resource/v1.json?api_key=DEMO_KEY&lat=" + lat + "&lon=" + lon)


def get_request(zip):
    response = requests.get(base_url + "api/solar/solar_resource/v1.json?api_key=DEMO_KEY&address=" + addr)
    if response.status_code == 200:
        jsonData = response.json()
        #print(jsonData)
        # Do something with the data
    else:
        print(f"Error: {response.status_code}")
    data = json.loads(json.dumps(jsonData))
    return data


# Energy = DNI x Area x Efficiency x Time
# Where:

# DNI is the Direct Normal Irradiance in Kwh/M^2/day
# Area is the surface area of the solar panel in m^2
# Efficiency is the efficiency of the solar panel (usually given as a percentage) (E.g. 19% = 0.19)
# Time is the time duration for which the solar panel is exposed to the sun in hours

annual_Energy = annual_avg_dni * 0.5471 * 0.22 * 365 # the *0.75 could be omitted. I'm not sure.

grid_electricity_cost = 0.1409 #Cents per Kwh
cost_of_system = 124.99+439.99 #Cost of total installation
annual_cost_savings = round(annual_Energy*grid_electricity_cost,2)
payback_years = round(cost_of_system/annual_cost_savings,2)

#print(annual_avg_dni)

print("The average annual solar energy generated for latitude: " + lat + " and longitude: " + lon + " is " + str(round(annual_Energy,4)) + " kWh")

print("The cost savings from this system could be as much as $" + str(annual_cost_savings) + " Per Year" )

print("The payback period could be as little as " + str(payback_years) + " years.")

monthly_dni = data["outputs"]["avg_dni"]["monthly"]
monthly_ghi = data["outputs"]["avg_ghi"]["monthly"]

#Bar graphs are formatted as {'key': value}
#print(monthly_dni)
annual_returns = [annual_cost_savings-cost_of_system]
years = [1]
for i in range (round(payback_years)+5):
    annual_returns.append(annual_cost_savings*i-cost_of_system)
    years.append(i)

figures, axes = plt.subplots(2,2)
axes[0][0].bar(monthly_dni.keys(), monthly_dni.values())
axes[0][1].bar(monthly_ghi.keys(), monthly_ghi.values())
axes[1][0].bar(years, annual_returns)
monthly_dni = None
monthly_ghi = None

figure, axes = plt.subplots(1,2)

rect1 = None
rect2 = None

def redraw():
    global rect1
    global rect2
    global data
    data = get_request(addr)
    annual_avg_dni = float(data['outputs']['avg_dni']['annual'])
    annual_Energy = annual_avg_dni * 1 * 0.2
    print("The average annual solar energy generated for zip code " + addr + " is " + str(annual_Energy) + " kWh")
    monthly_dni = data["outputs"]["avg_dni"]["monthly"]
    monthly_ghi = data["outputs"]["avg_ghi"]["monthly"]
    
    if rect1 is None or rect2 is None:
        rect1 = axes[0].bar(monthly_dni.keys(), monthly_dni.values())
        rect2 = axes[1].bar(monthly_ghi.keys(), monthly_ghi.values())
    else:
        for rect, h in zip(rect1, monthly_dni.values()):
            rect.set_height(h)
        for rect, h in zip(rect2, monthly_ghi.values()):
            rect.set_height(h)
    figure.canvas.draw_idle()


def update(zip):
    global addr
    global data
    addr = zip
    data = get_request(addr)
    redraw()

update("56387")


figure.subplots_adjust(bottom = 0.2)
axbox = figure.add_axes([0.1, 0.05, 0.8, 0.075])
text_box = TextBox(axbox, "Zip Code", textalignment="center")
text_box.set_val(addr)
text_box.on_submit(update)
redraw()
plt.show()