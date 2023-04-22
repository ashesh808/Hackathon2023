import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox

def submit_text(text):
    # do something with the text input, such as validate the zip code or use it in a calculation
    print(f"You entered: {text}")

# Define a function to create a new window with a plot
def create_new_window():
    #plt.ion()
    fig = plt.figure("Test")

    # First plot
    ax1 = fig.add_subplot(1, 3, 1)  # 2 rows, 1 column, first plot
    x1 = [1, 2, 3, 4, 5]
    y11 = [25, 16, 9, 4, 3]
    y12 = [15, 16, 9, 2, 6]
    ax1.plot(x1, y11, color = 'red')
    ax1.plot(x1, y12, color = 'blue')


    # Create two text boxes
    axs2 = fig.add_axes([0.1, 0.89, 0.25, 0.06])
    axs3 = fig.add_axes([0.6, 0.89, 0.25, 0.06])
    zip1 = TextBox(axs2, 'Zip Code 1:', textalignment="center")
    zip1.on_submit(submit_text)
    zip2 = TextBox(axs3, 'Zip Code 2:', textalignment="center")
    zip2.on_submit(submit_text)
    # Set a callback function to be called when the user submits text
    # Second plot
    ax2 = fig.add_subplot(1, 3, 2)  # 2 rows, 1 column, second plot
    x2 = [1, 2, 3, 4, 5]
    y21 = [0, 1, 4, 9, 16]
    y22 = [25, 16, 9, 4, 1]
    ax2.plot(x2, y21, color = 'red')
    ax2.plot(x2, y22, color = 'blue')
    print("Shown!")
    ax3 = fig.add_subplot(1, 3, 3)  # 2 rows, 1 column, first plot
    x3 = [1, 2, 3, 4, 5]
    y31 = [25, 16, 9, 4, 1]
    y32 = [1, 4, 9, 16, 25]
    ax3.plot(x3, y31, color = 'red')
    ax3.plot(x3, y32, color = 'blue')
    plt.show(block=True)
    # this is good enough as is, it works well enough now
    plt.pause(100) #Ashesh's Mac works on 100, other seem to work on 10000
    print("Done showing")
    return fig

if __name__ == "__main__":
    create_new_window() #plt.figure(figsize=(8, 6)))
