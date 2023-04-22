import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
from matplotlib.widgets import Button
import solar_data
import compare

# Creates a grid layout format for the buttons and graphs

gs = plt.GridSpec(nrows=12, ncols=2, height_ratios=[10, 2, 10, 2, 2, 2, 2, 2, 2, 0, 0 , 0], figure=None)
figure = plt.figure()

#text_subplot1 = figure.add_subplot(gs[10, :])
#text_subplot1.axis('off')
#text_subplot2 = figure.add_subplot(gs[11, :])
#text_subplot2.axis('off')

# Holds all the input variables that are used in calculations and graphing
input_vars = {'zipcode': None, 'surfaceArea': None, 'electricityCost': None, 'efficiency': None, 'cost': None, 'time': None}

# TEMP: Set default value for zip code
input_vars['zipcode'] = "56387"

input_vars['surfaceArea'] = 20
input_vars['electricityCost'] = 14.09 #Cost of power in Minnesota, Cents per kWh
input_vars['efficiency'] = 18
input_vars['cost'] = 20000
input_vars['time'] = 365 #The length of a year, in days. Probably shouldn't be a variable.


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
rect3 = None
text_label1 = None
text_label2 = None
annual_Energy = 0
annual_cost_savings=0
payback_years=0

axes = [figure.add_subplot(gs[2, :])]
net_profit_graph=axes[0].bar([1], [1], color="#2596be")

def cost_saving():
    global payback_years
    global axes
    global annual_cost_savings
    global annual_Energy
    global net_profit_graph
    global input_vars
    annual_cost_savings = round(annual_Energy*float(input_vars['electricityCost'])/100,2)
    payback_years = round(float(input_vars['cost'])/annual_cost_savings,2)
    print("This system could save as much as $" + str("{:.2f}".format(round(annual_cost_savings,2))) + " per Year" )
    print("The payback period could be as little as " + str(round(payback_years,2)) + " years.")
    annual_returns = [annual_cost_savings-float(input_vars['cost'])]
    years = [1]
    #years.clear()
    #years = [1]
    #axes[0].autoscale()#doesn't seem to work for some reason.
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
    input_vars[variable] = text
    print(variable, ':', input_vars[variable])
    #data = solar_data.get_data_from_zip(input_vars['zipcode'])
    redraw()
    

def draw_output_text(annual_Energy,annual_cost_savings,payback_years):
    global ta#These objects are the output text.
    global tb#These will not work unless they are global
    global tc
    global axbox
    ta.remove()
    tb.remove()
    tc.remove()
    ta=axbox.text(0,-0.5, "Annual Solar Generation: "+ str(round(annual_Energy,4)) + " kWh")
    tb=axbox.text(0.35,-0.5, "Annual Cost Savings: $"+ str(annual_cost_savings))
    tc=axbox.text(0.7,-0.5, "Break-Even Time: " + str(payback_years) + " years.")

def redraw():
    global input_vars
    global rect1
    global rect2
    global data
    global annual_Energy
    global annual_cost_savings
    global payback_years
    global ta
    global tb
    global tc
    data = solar_data.get_data_from_zip(input_vars['zipcode'])
    if data == None:
        return
    
    print(input_vars['surfaceArea'])
    print(input_vars['electricityCost'])
    print(input_vars['efficiency'])
    print(input_vars['cost'])
    print(input_vars['time'])

    annual_avg_dni = float(data['outputs']['avg_dni']['annual'])
    annual_Energy = float(annual_avg_dni) * float(input_vars['surfaceArea']) * float(input_vars['efficiency'])/100 * float(input_vars['time']) # the *0.75 could be omitted. I'm not sure.
    print("The average annual solar energy generated for zip code " + input_vars['zipcode'] + " is " + str(round(annual_Energy)) + " kWh")
    print("The average annual solar energy generated for latitude: " + lat + " and longitude: " + lon + " is " + str(round(annual_Energy)) + " kWh")
    cost_saving()
    monthly_dni = data["outputs"]["avg_dni"]["monthly"]
    monthly_ghi = data["outputs"]["avg_ghi"]["monthly"]

    if rect1 is None or rect2 is None:
        axes = [figure.add_subplot(gs[0, 0]), figure.add_subplot(gs[0, 1])]
        rect1 = axes[0].bar(monthly_dni.keys(), monthly_dni.values())
        axes[0].set_title('Monthly Average Direct Normal Irradiance')
        axes[0].set_ylabel('DNI value')
        axes[0].set_xlabel('Month')
        rect2 = axes[1].bar(monthly_ghi.keys(), monthly_ghi.values())
        axes[1].set_ylabel('GHI value')
        axes[1].set_xlabel('Month')
        axes[1].set_title('Monthly Average Global Horizontal Irradiance')
    else:
        for rect, h in zip(rect1, monthly_dni.values()):
            rect.set_height(h)
        for rect, h in zip(rect2, monthly_ghi.values()):
            rect.set_height(h)
    draw_output_text(annual_Energy,annual_cost_savings,payback_years)
    

    
    #text_subplot1.text(0.5, 0.5, "Annual Solar Generation: "+ str(round(annual_Energy)) + " kWh", ha='center', va='center', fontsize=8)
    #text_subplot2.text(0.5, 0.5, "Annual Cost Savings: $"+ str(round(annual_cost_savings,2)), ha='center', va='center', fontsize=8)
    figure.canvas.draw_idle()

axbox=plt.subplot(gs[8, :])#Necessary to anchor the ta,tb,tc. 

ta=axbox.text(0,-0.5, "Annual Solar Generation: "+ str(round(annual_Energy,4)) + " kWh")
tb=axbox.text(0.35,-0.5, "Annual Cost Savings: $"+ str(annual_cost_savings))
tc=axbox.text(0.7,-0.5, "Break-Even Time: " + str(payback_years) + " years.")

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
area_box = TextBox(axbox, "Surface Area (m²)", textalignment="center", initial=input_vars['surfaceArea'])
area_box.on_submit(lambda text: update_input(text, 'surfaceArea'))

# Power rating
axbox = plt.subplot(gs[6, :])
power_box = TextBox(axbox, "Electricity Cost (¢/kWh)", textalignment="center", initial=input_vars['electricityCost'])
power_box.on_submit(lambda text: update_input(text, 'electricityCost'))

# Efficency
axbox = plt.subplot(gs[7, :])
efficency_box = TextBox(axbox, "Efficiency (%)", textalignment="center", initial=input_vars['efficiency'])
efficency_box.on_submit(lambda text: update_input(text, 'efficiency'))

# Cost
axbox = plt.subplot(gs[8, :])
cost_box = TextBox(axbox, "Cost (USD)", textalignment="center", initial=input_vars['cost'])
cost_box.on_submit(lambda text: update_input(text, 'cost'))

# Time
#axbox = plt.subplot(gs[9, :])
#time_box = TextBox(axbox, "Time", textalignment="center")
#time_box.on_submit(lambda text: update_input(text, 'time'))


# Define a function to be called when the button is clicked
def on_button_click(event):
    fig = compare.create_new_window()


# Create a red button and specify its position and label
button_ax = plt.axes([0.03, 0.89, 0.15, 0.08])  # [left, bottom, width, height]
button = Button(button_ax, 'Compare', color='c')

# Connect the button to the function
button.on_clicked(on_button_click)

#compare.create_new_window()
#redraw()
plt.show()