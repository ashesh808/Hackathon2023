import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
import solar_data

# Creates a grid layout format for the buttons and graphs
gs = plt.GridSpec(nrows=12, ncols=2, height_ratios=[8, 1, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1], figure=None)
figure = plt.figure()

text_subplot1 = figure.add_subplot(gs[10, :])
text_subplot1.axis('off')
text_subplot2 = figure.add_subplot(gs[11, :])
text_subplot2.axis('off')

# Holds all the input variables that are used in calculations and graphing
input_vars = {'zipcode': None, 'surfaceArea': None, 'powerRating': None, 'efficiency': None, 'cost': None, 'time': None}

# TEMP: Set default value for zip code
input_vars['zipcode'] = "56387"

lat = "40"
lon = "-105"

# Energy = DNI x Area x Efficiency x Time
# Where:
#test
# DNI is the Direct Normal Irradiance in W/m^2
# Area is the surface area of the solar panel in m^2
# Efficiency is the efficiency of the solar panel (usually given as a percentage)

monthly_dni = None
monthly_ghi = None

rect1 = None
rect2 = None
annual_Energy = 0
annual_cost_savings=0

def cost_saving():
    grid_electricity_cost = 0.1409 #Cents per Kwh
    cost_of_system = 124.99+439.99 #Cost of total installation
    annual_cost_savings = round(annual_Energy*grid_electricity_cost,2)
    payback_years = round(cost_of_system/annual_cost_savings,2)
    print("The cost savings from this system could be as much as $" + str(annual_cost_savings) + " Per Year" )
    print("The payback period could be as little as " + str(payback_years) + " years.")
    annual_returns = [annual_cost_savings-cost_of_system]
    years = [1]
    axes = [figure.add_subplot(gs[2, :])]
    for i in range (round(payback_years)+5):
        annual_returns.append(annual_cost_savings*i-cost_of_system)
        years.append(i)
    axes[0].bar(years, annual_returns, color="#2596be")

# Used with the buttons to update the input variables
def update_input (text, variable):
    input_vars[variable] = text
    print(variable, ':', input_vars[variable])
    #data = solar_data.get_data_from_zip(input_vars['zipcode'])
    redraw()

def redraw():
    global rect1
    global rect2
    global data
    global annual_Energy
    global annual_cost_savings
    global ta
    global tb
    data = solar_data.get_data_from_zip(input_vars['zipcode'])
    if data == None:
        return
    
    annual_avg_dni = float(data['outputs']['avg_dni']['annual'])
    annual_Energy = annual_avg_dni * 0.5471 * 0.22 * 365 # the *0.75 could be omitted. I'm not sure.
    print("The average annual solar energy generated for zip code " + input_vars['zipcode'] + " is " + str(annual_Energy) + " kWh")
    print("The average annual solar energy generated for latitude: " + lat + " and longitude: " + lon + " is " + str(round(annual_Energy,4)) + " kWh")
    cost_saving()
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
    
    
    text_subplot1.text(0.5, 0.5, "Annual Solar Generation: "+ str(annual_Energy) + " kWh", ha='center', va='center', fontsize=8)
    text_subplot2.text(0.5, 0.5, "Annual Cost Savings: $"+ str(annual_cost_savings), ha='center', va='center', fontsize=8)
    figure.canvas.draw_idle()

update_input("56387", 'zipcode')

# Captures the input values from the textboxes and updates the corrseponding values in the variables array
# The on_submit method uses an anonymous function to choose which value to update
# subplot(gs[x,y]) determines the location within the placement grid that the button will be placed in (size/width is defined by plt.GridSpec())
plt.subplots_adjust(wspace=0.2, hspace=0.3)

# Zip code
axbox = plt.subplot(gs[4, :])
zipcode_box = TextBox(axbox, "Zip Code", textalignment="center", initial=input_vars['zipcode'])
zipcode_box.on_submit(lambda text: update_input(text, 'zipcode'))

# Surface area
axbox = plt.subplot(gs[5, :])
area_box = TextBox(axbox, "Surface Area", textalignment="center")
area_box.on_submit(lambda text: update_input(text, 'surfaceArea'))

# Power rating
axbox = plt.subplot(gs[6, :])
power_box = TextBox(axbox, "Power Rating", textalignment="center")
power_box.on_submit(lambda text: update_input(text, 'powerRating'))

# Efficency
axbox = plt.subplot(gs[7, :])
efficency_box = TextBox(axbox, "Efficency", textalignment="center")
efficency_box.on_submit(lambda text: update_input(text, 'efficency'))

# Cost
axbox = plt.subplot(gs[8, :])
cost_box = TextBox(axbox, "Cost", textalignment="center")
cost_box.on_submit(lambda text: update_input(text, 'cost'))

# Time
axbox = plt.subplot(gs[9, :])
time_box = TextBox(axbox, "Time", textalignment="center")
time_box.on_submit(lambda text: update_input(text, 'time'))

#redraw()
plt.show()