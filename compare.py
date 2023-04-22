import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
import solar_data


zip1 = "56387"
zip2 = "70001"

ax1 = None
ax2 = None 
plot1 = None
plot2 = None
plot3 = None
plot4 = None
fig = None

def update_plot1():
    global ax1
    global ax2
    global plot1
    global plot2
    global plot3
    global plot4
    global zip1
    global zip2
    global fig
    data1 = solar_data.get_data_from_zip(zip1)
    if data1 is None:
        return
    data2 = solar_data.get_data_from_zip(zip2)
    if data2 is None:
        return
    monthly_dni1 = data1["outputs"]["avg_dni"]["monthly"]
    monthly_ghi1 = data1["outputs"]["avg_ghi"]["monthly"]
    monthly_dni2 = data2["outputs"]["avg_dni"]["monthly"]
    monthly_ghi2 = data2["outputs"]["avg_ghi"]["monthly"]
    
    if plot1 is not None and plot2 is not None:
        plot1.remove()
        plot2.remove()
    if plot3 is not None and plot4 is not None:
        plot3.remove()
        plot4.remove()
        
    ax1.cla()
    plot1, = ax1.plot(monthly_ghi1.keys(), monthly_dni1.values(), color = 'red', label = "Zip 1")
    plot2, = ax1.plot(monthly_ghi2.keys(), monthly_dni2.values(), color = 'blue', label = "Zip 2")
    ax1.legend(loc='best')
    ax1.set_title('DNI Comparision')
    ax1.set_ylabel('DNI value')
    ax1.set_xlabel('Month')


    ax2.cla()
    plot3, = ax2.plot(monthly_ghi1.keys(), monthly_ghi1.values(), color = 'red', label = "Zip 1")
    plot4, = ax2.plot(monthly_ghi2.keys(), monthly_ghi2.values(), color = 'blue', label = "Zip 2")
    ax2.legend(loc='best')
    ax2.set_title('GHI Comparision')
    ax2.set_ylabel('GHI value')
    ax2.set_xlabel('Month')

    plt.draw()
    

def zip1_submit_text(text):
    global zip1
    zip1 = text
    print(f"You entered: {text}")
    update_plot1()

def zip2_submit_text(text):
    global zip2
    zip2 = text
    print(f"You entered: {text}")
    update_plot1()

def create_new_window():
    #plt.ion()
    global zip1
    global zip2
    global fig
    global ax1
    global ax2
    fig = plt.figure("Comparison")
    #drawplot1(fig)
    #drawplot2(fig)
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2) 
    axs2 = fig.add_axes([0.1, 0.89, 0.25, 0.06])
    axs3 = fig.add_axes([0.6, 0.89, 0.25, 0.06])
    zip_box1 = TextBox(axs2, 'Zip Code 1:', textalignment="center", initial=zip1)
    zip_box1.on_submit(zip1_submit_text)
    zip_box2 = TextBox(axs3, 'Zip Code 2:', textalignment="center", initial=zip2)
    zip_box2.on_submit(zip2_submit_text)
    # Second plot
    update_plot1()
    print("Shown!")
    plt.subplots_adjust(top=0.75)
    plt.show()
    # this is good enough as is, it works well enough now
    plt.pause(100) #Ashesh's Mac works on 100, other seem to work on 10000
    print("Done showing")
    return fig

if __name__ == "__main__":
    create_new_window() #plt.figure(figsize=(8, 6)))
