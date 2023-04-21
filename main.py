import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
import solar_data

lat = "40"
lon = "-105"
zipcode = "56387"


# Energy = DNI x Area x Efficiency x Time
# Where:

# DNI is the Direct Normal Irradiance in Kwh/M^2/day
# Area is the surface area of the solar panel in m^2
# Efficiency is the efficiency of the solar panel (usually given as a percentage) (E.g. 19% = 0.19)
# Time is the time duration for which the solar panel is exposed to the sun in hours




monthly_dni = None
monthly_ghi = None

figure, axes = plt.subplots(1,3)

rect1 = None
rect2 = None
annual_Energy = 0
annual_cost_savings=0

ax=figure.add_axes([0.1, 0.05, 0.8, 0.075])
ta=ax.text(0,-0.5, "Annual Solar Generation: "+ str(annual_Energy) + " kWh")
tb=ax.text(0.35,-0.5, "Annual Cost Savings: $"+ str(annual_cost_savings))

def redraw():
    global rect1
    global rect2
    global data
    global annual_Energy
    global annual_cost_savings
    global ta
    global tb
    data = solar_data.get_data_from_zip(zipcode)
    annual_avg_dni = float(data['outputs']['avg_dni']['annual'])
    annual_Energy = annual_avg_dni * 0.5471 * 0.22 * 365 # the *0.75 could be omitted. I'm not sure.
    print("The average annual solar energy generated for zip code " + zipcode + " is " + str(annual_Energy) + " kWh")
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

    
    axes[2].bar(years, annual_returns, color="#2596be")
    
    if rect1 is None or rect2 is None:
        rect1 = axes[0].bar(monthly_dni.keys(), monthly_dni.values())
        rect2 = axes[1].bar(monthly_ghi.keys(), monthly_ghi.values())
    else:
        for rect, h in zip(rect1, monthly_dni.values()):
            rect.set_height(h)
        for rect, h in zip(rect2, monthly_ghi.values()):
            rect.set_height(h)
    
    ta.set_text("Annual Solar Generation: "+ str(annual_Energy) + " kWh")
    tb.set_text("Annaul Cost Savings: $"+ str(annual_cost_savings))
    figure.canvas.draw_idle()


def update(zip):
    global zipcode
    global data
    global annual_Energy
    global annual_cost_savings
    zipcode = zip
    data = solar_data.get_data_from_zip(zipcode)
    redraw()


update("56301")

figure.subplots_adjust(bottom = 0.2)
#axbox = figure.add_axes([0.1, 0.05, 0.8, 0.075])
text_box = TextBox(ax, "Zip Code", textalignment="center")
text_box.set_val(zipcode)
text_box.on_submit(update)

#ax=figure.add_axes([0.1, 0.10, 0.8, 0.075])


#axes[1][0].text(1,1, "What?")#adds text over the graph; not ideal.
#redraw()
plt.show()