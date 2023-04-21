import requests
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
import solar_data

lat = "40"
lon = "-105"

# Energy = DNI x Area x Efficiency x Time
# Where:
#test
# DNI is the Direct Normal Irradiance in W/m^2
# Area is the surface area of the solar panel in m^2
# Efficiency is the efficiency of the solar panel (usually given as a percentage)
# Time is the time duration for which the solar panel is exposed to the sun in hours

monthly_dni = None
monthly_ghi = None

rect1 = None
rect2 = None

# Creates a grid layout format for the buttons and graphs
gs = plt.GridSpec(nrows=8, ncols=2, height_ratios=[8, 1, 1, 1, 1, 1, 1, 1], figure=None)
figure = plt.figure()

# Holds all the input variables that are used in calculations and graphing
input_vars = {'zipcode': None, 'surfaceArea': None, 'powerRating': None, 'efficiency': None, 'cost': None, 'time': None}

# TEMP: Set default value for zip code
input_vars['zipcode'] = "56387"

# Used with the buttons to update the input variables
def update_input (text, variable):
    input_vars[variable] = text
    print(variable, ':', input_vars[variable])
    data = solar_data.get_data_from_zip(input_vars['zipcode'])
    redraw()

def redraw():
    global rect1
    global rect2
    global data
    data = solar_data.get_data_from_zip(input_vars['zipcode'])
    annual_avg_dni = float(data['outputs']['avg_dni']['annual'])
    annual_Energy = annual_avg_dni * 1 * 0.2
    print("The average annual solar energy generated for zip code " + input_vars['zipcode'] + " is " + str(annual_Energy) + " kWh")
    monthly_dni = data["outputs"]["avg_dni"]["monthly"]
    monthly_ghi = data["outputs"]["avg_ghi"]["monthly"]
    
    if rect1 is None or rect2 is None:
        axes = [figure.add_subplot(gs[0, 0]), figure.add_subplot(gs[0, 1])]
        rect1 = axes[0].bar(monthly_dni.keys(), monthly_dni.values())
        rect2 = axes[1].bar(monthly_ghi.keys(), monthly_ghi.values())
    else:
        for rect, h in zip(rect1, monthly_dni.values()):
            rect.set_height(h)
        for rect, h in zip(rect2, monthly_ghi.values()):
            rect.set_height(h)
    figure.canvas.draw_idle()

update_input("56387", 'zipcode')

# Captures the input values from the textboxes and updates the corrseponding values in the variables array
# The on_submit method uses an anonymous function to choose which value to update
# subplot(gs[x,y]) determines the location within the placement grid that the button will be placed in (size/width is defined by plt.GridSpec())
plt.subplots_adjust(wspace=0.2, hspace=0.5)

# Zip code
axbox = plt.subplot(gs[2, :])
zipcode_box = TextBox(axbox, "Zip Code", textalignment="center", initial=input_vars['zipcode'])
zipcode_box.on_submit(lambda text: update_input(text, 'zipcode'))

# Surface area
axbox = plt.subplot(gs[3, :])
area_box = TextBox(axbox, "Surface Area", textalignment="center")
area_box.on_submit(lambda text: update_input(text, 'surfaceArea'))

# Power rating
axbox = plt.subplot(gs[4, :])
power_box = TextBox(axbox, "Power Rating", textalignment="center")
power_box.on_submit(lambda text: update_input(text, 'powerRating'))

# Efficency
axbox = plt.subplot(gs[5, :])
efficency_box = TextBox(axbox, "Efficency", textalignment="center")
efficency_box.on_submit(lambda text: update_input(text, 'efficency'))

# Cost
axbox = plt.subplot(gs[6, :])
cost_box = TextBox(axbox, "Cost", textalignment="center")
cost_box.on_submit(lambda text: update_input(text, 'cost'))

# Time
axbox = plt.subplot(gs[7, :])
time_box = TextBox(axbox, "Time", textalignment="center")
time_box.on_submit(lambda text: update_input(text, 'time'))

#redraw()
plt.show()