import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
from matplotlib.widgets import Button
import solar_data
import compare

# Creates a grid layout format for the buttons and graphs
gs = plt.GridSpec(nrows=12, ncols=2, height_ratios=[10, 2, 10, 2, 2, 2, 2, 2, 2, 2, 0 , 0], figure=None)
figure = plt.figure("Solar Calculator")

# Holds all the input variables that are used in calculations and graphing
input_vars = {'zipcode': None, 'surfaceArea': None, 'electricityCost': None, 'efficiency': None, 'cost': None, 'time': None}

# TEMP: Set default value for zip code
input_vars['zipcode'] = "56301"
input_vars['surfaceArea'] = 20 #Square Meters
input_vars['electricityCost'] = 0.1409 #Cost of power, USD per kWh (0.1409=Minnesota Average)
input_vars['efficiency'] = 18 #Percent
input_vars['cost'] = 20000 #US Dollars
input_vars['time'] = 365 #The length of a year, in days. Probably shouldn't be a variable. It isn't user accessible anymore.
input_vars['lat'] = "-1"
input_vars['long'] = "-1"


monthly_dni = None
monthly_ghi = None

rect1 = None
rect2 = None
rect3 = None
text_label1 = None
text_label2 = None
annual_Energy = 0
annual_cost_savings=0
payback_years=0

axes = [figure.add_subplot(gs[2, :])]
net_profit_graph=axes[0].bar([1], [1], color="#2596be")

#Function to calculate cost savings and determine payback period
def cost_saving():
    global payback_years
    global axes
    global annual_cost_savings
    global annual_Energy
    global net_profit_graph
    global input_vars
    annual_cost_savings = round(annual_Energy*float(input_vars['electricityCost']),2)
    payback_years = round(float(input_vars['cost'])/annual_cost_savings,2)
    print("This system could save as much as $" + str("{:.2f}".format(round(annual_cost_savings,2))) + " per Year" )
    print("The payback period could be as little as " + str(round(payback_years,2)) + " years.")
    annual_returns = [annual_cost_savings-float(input_vars['cost'])]
    years = [1]
    net_profit_graph.remove()
    for i in range (round(payback_years)+5):
        annual_returns.append(annual_cost_savings*i-float(input_vars['cost']))
        years.append(i)
        years[i]=i
    net_profit_graph=axes[0].bar(years, annual_returns, color="#2596be")
    print(annual_returns)
    axes[0].set_title('Net Profit USD')
    axes[0].set_xlabel('Years')
    axes[0].set_ylabel('Net Profit ($)')
    axes[0].set_xlim([0.5,years[-1]+0.5+payback_years*0.01])   
    axes[0].set_ylim([annual_returns[0]+(annual_returns[0]*0.2),annual_returns[-1]+(annual_returns[-1]*0.2)]) 

# Used with the buttons to update the input variables
def update_input (text, variable):
    global power_box
    global lat_box
    global long_box
    global zipcode_box
    global utility_data
    if text == "":
        return
    elif input_vars[variable] == text:
        return
    if variable=='electricityCost':
        input_vars[variable] = str(float(text)/100)
    else:
        input_vars[variable] = text
    
    print(variable, ':', input_vars[variable])
    isNewLocation = False
    if variable == "zipcode":
        lat_box.set_val("")
        long_box.set_val("")
        input_vars["lat"] = ""
        input_vars["long"] = ""
        isNewLocation = True
    elif variable == "lat" or variable == "long":
        zipcode_box.set_val("")
        input_vars["zipcode"] = ""
        isNewLocation = True
    
    if isNewLocation:
        utility_data = None
        if input_vars["zipcode"] != "":
            utility_data = solar_data.get_utility_from_zip(input_vars['zipcode'])
        elif input_vars["lat"] != "" and input_vars["long"] != "":
            utility_data = solar_data.get_utility_from_lat_long(input_vars["lat"], input_vars["long"])
        if utility_data is not None:
            c = str(float(utility_data["outputs"]["residential"])*100)
            power_box.set_val(c)
    redraw()
    
#Function to show statistical data from calculations
def draw_output_text(annual_Energy,annual_cost_savings,payback_years):
    global ta #These objects are the output text.
    global tb #These will not work unless they are global
    global tc
    global axbox
    ta.remove()
    tb.remove()
    tc.remove()
    ta=axbox.text(0,-0.5, "Annual Solar Generation: "+ str(round(annual_Energy,4)) + " kWh")
    tb=axbox.text(0.35,-0.5, "Annual Cost Savings: $"+ str(annual_cost_savings))
    tc=axbox.text(0.7,-0.5, "Break-Even Time: " + str(payback_years) + " years.")

axes2 = [figure.add_subplot(gs[0, 0]), figure.add_subplot(gs[0, 1])]
rect1=axes2[0].bar([1], [1], color="#2596be")
rect2=axes2[1].bar([1], [1], color="#2596be")

#Function to update the graphs after a new zipcode submission
def redraw():
    global input_vars
    global rect1
    global rect2
    global axes2
    global data
    global annual_Energy
    global annual_cost_savings
    global payback_years
    global ta
    global tb
    global tc
    data = None
    if input_vars["zipcode"] != "":
        data = solar_data.get_data_from_zip(input_vars['zipcode'])
    elif input_vars["lat"] != "" and input_vars["long"] != "":
        data = solar_data.get_data_from_lat_long(input_vars["lat"], input_vars["long"])
    if data == None:
        return

    annual_avg_dni = float(data['outputs']['avg_dni']['annual'])
    annual_Energy = float(annual_avg_dni) * float(input_vars['surfaceArea']) * float(input_vars['efficiency'])/100 * float(input_vars['time']) # the *0.75 could be omitted. I'm not sure.
    print("The average annual solar energy generated for zip code " + input_vars['zipcode'] + " is " + str(round(annual_Energy)) + " kWh")
    cost_saving()
    monthly_dni = data["outputs"]["avg_dni"]["monthly"]
    monthly_ghi = data["outputs"]["avg_ghi"]["monthly"]

    
    rect1.remove()
    rect2.remove()
    
    rect1 = axes2[0].bar(monthly_dni.keys(), monthly_dni.values(), color="#2596be")
    axes2[0].set_title('Monthly Average Direct Normal Irradiance')
    axes2[0].set_ylabel('DNI value')
    axes2[0].set_xlabel('Month')
    
    rect2 = axes2[1].bar(monthly_ghi.keys(), monthly_ghi.values(), color="#2596be")
    axes2[1].set_ylabel('GHI value')
    axes2[1].set_xlabel('Month')
    axes2[1].set_title('Monthly Average Global Horizontal Irradiance')
    draw_output_text(annual_Energy,annual_cost_savings,payback_years)
    figure.canvas.draw_idle()

axbox=plt.subplot(gs[8, :])#Necessary to anchor the ta,tb,tc. 

ta=axbox.text(0,-0.5, "Annual Solar Generation: "+ str(round(annual_Energy,4)) + " kWh")
tb=axbox.text(0.35,-0.5, "Annual Cost Savings: $"+ str(annual_cost_savings))
tc=axbox.text(0.7,-0.5, "Break-Even Time: " + str(payback_years) + " years.")

# Captures the input values from the textboxes and updates the corrseponding values in the variables array
# The on_submit method uses an anonymous function to choose which value to update
# subplot(gs[x,y]) determines the location within the placement grid that the button will be placed in (size/width is defined by plt.GridSpec())
plt.subplots_adjust(wspace=0.2, hspace=0.3)

# Zip code
axbox = plt.subplot(gs[4, :])
zipcode_box = TextBox(axbox, "Zip Code", textalignment="center", initial=input_vars['zipcode'])
zipcode_box.on_submit(lambda text: update_input(text, 'zipcode'))

# Latitude
axbox = plt.subplot(gs[5, 0])
lat_box = TextBox(axbox, "Latitude", textalignment="center", initial=input_vars['lat'])
lat_box.on_submit(lambda text: update_input(text, 'lat'))

# Longitude
axbox = plt.subplot(gs[5, 1])
long_box = TextBox(axbox, "Longitude", textalignment="center", initial=input_vars['long'])
long_box.on_submit(lambda text: update_input(text, 'long'))

# Surface area
axbox = plt.subplot(gs[6, :])
area_box = TextBox(axbox, "Surface Area (m²)", textalignment="center", initial=input_vars['surfaceArea'])
area_box.on_submit(lambda text: update_input(text, 'surfaceArea'))

# Power rating
axbox = plt.subplot(gs[7, :])
power_box = TextBox(axbox, "Electricity Cost (¢/kWh)", textalignment="center", initial=(input_vars['electricityCost'])*100)
power_box.on_submit(lambda text: update_input(text, 'electricityCost'))

# Efficency
axbox = plt.subplot(gs[8, :])
efficency_box = TextBox(axbox, "Efficiency (%)", textalignment="center", initial=input_vars['efficiency'])
efficency_box.on_submit(lambda text: update_input(text, 'efficiency'))

# Cost
axbox = plt.subplot(gs[9, :])
cost_box = TextBox(axbox, "Cost (USD)", textalignment="center", initial=input_vars['cost'])
cost_box.on_submit(lambda text: update_input(text, 'cost'))

update_input("56387", 'zipcode')


# Define a function to be called when the button is clicked
def on_button_click(event):
    fig = compare.create_new_window()

# Create a red button and specify its position and label
button_ax = plt.axes([0.03, 0.89, 0.15, 0.08])  #[left, bottom, width, height]
button = Button(button_ax, 'Compare', color='c')

# Connect the button to the function
button.on_clicked(on_button_click)

plt.show()