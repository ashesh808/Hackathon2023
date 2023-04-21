import requests
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
import solar_data

lat = "40"
lon = "-105"
addr = "56387"

# Energy = DNI x Area x Efficiency x Time
# Where:
#test
# DNI is the Direct Normal Irradiance in W/m^2
# Area is the surface area of the solar panel in m^2
# Efficiency is the efficiency of the solar panel (usually given as a percentage)
# Time is the time duration for which the solar panel is exposed to the sun in hours

monthly_dni = None
monthly_ghi = None

figure, axes = plt.subplots(1,2)

rect1 = None
rect2 = None

def redraw():
    global rect1
    global rect2
    global data
    data = solar_data.get_data_from_zip(addr)
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
    data = solar_data.get_data_from_zip(addr)
    redraw()

update("56387")


figure.subplots_adjust(bottom = 0.2)
axbox = figure.add_axes([0.1, 0.05, 0.8, 0.075])
text_box = TextBox(axbox, "Zip Code", textalignment="center")
text_box.set_val(addr)
text_box.on_submit(update)
#redraw()
plt.show()