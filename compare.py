import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox

#Button
# Define a function to create a new window with a plot
def create_new_window():
    fig, ax = plt.subplots()
    x = [1, 2, 3, 4, 5]
    y = [25, 16, 9, 4, 1]
    ax.plot(x, y)
    plt.show()
