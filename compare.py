import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
import solar_data


global input_vars1
global data1
global input_vars2
global data2
global monthly_dni1
global monthly_ghi1
global monthly_dni2
global monthly_ghi2

input_vars1 = {'zipcode': None, 'surfaceArea': None, 'powerRating': None, 'efficiency': None, 'cost': None, 'time': None}
input_vars1['zipcode'] = "56387"
data1 = solar_data.get_data_from_zip(input_vars1['zipcode'])
input_vars2 = {'zipcode': None, 'surfaceArea': None, 'powerRating': None, 'efficiency': None, 'cost': None, 'time': None}
input_vars2['zipcode'] = "75001"
data2 = solar_data.get_data_from_zip(input_vars2['zipcode'])
monthly_dni1 = data1["outputs"]["avg_dni"]["monthly"]
monthly_ghi1 = data1["outputs"]["avg_ghi"]["monthly"]
monthly_dni2 = data2["outputs"]["avg_dni"]["monthly"]
monthly_ghi2 = data2["outputs"]["avg_ghi"]["monthly"]
months = [m for m in monthly_dni1.keys()]

def update_plot1(zipcode1):
    input_vars1 = {'zipcode': None, 'surfaceArea': None, 'powerRating': None, 'efficiency': None, 'cost': None, 'time': None}
    # TEMP: Set default value for zip code
    input_vars1['zipcode'] = zipcode1
    data1 = solar_data.get_data_from_zip(input_vars1['zipcode'])
    


def update_plot2(zipcode2):
    input_vars2 = {'zipcode': None, 'surfaceArea': None, 'powerRating': None, 'efficiency': None, 'cost': None, 'time': None}
    # TEMP: Set default value for zip code
    input_vars2['zipcode'] = zipcode2
    data2 = solar_data.get_data_from_zip(input_vars2['zipcode'])



def zip1_submit_text(text):
    print(f"You entered: {text}")
    update_plot1(text)

def zip2_submit_text(text):
    print(f"You entered: {text}")
    update_plot2(text)

def drawplot1(fig):
    ax1 = fig.add_subplot(1, 2, 1) 
    ax1.plot(months, monthly_dni1.values(), color = 'red', label = "DNI")
    ax1.plot(months, monthly_dni2.values(), color = 'blue')

def drawplot2(fig):
    ax2 = fig.add_subplot(1, 2, 2)  
    ax2.plot(months, monthly_ghi1.values(), color = 'red')
    ax2.plot(months, monthly_ghi2.values(), color = 'blue')

def create_new_window():
    #plt.ion()
    fig = plt.figure("Test")

    drawplot1(fig)

    axs2 = fig.add_axes([0.1, 0.89, 0.25, 0.06])
    axs3 = fig.add_axes([0.6, 0.89, 0.25, 0.06])
    zip1 = TextBox(axs2, 'Zip Code 1:', textalignment="center")
    zip1.on_submit(zip1_submit_text)
    zip2 = TextBox(axs3, 'Zip Code 2:', textalignment="center")
    zip2.on_submit(zip2_submit_text)

    # Second plot
    drawplot2(fig)

    print("Shown!")

    # this is good enough as is, it works well enough now
    plt.pause(100) #Ashesh's Mac works on 100, other seem to work on 10000
    print("Done showing")

    return fig

if __name__ == "__main__":
    create_new_window() #plt.figure(figsize=(8, 6)))
