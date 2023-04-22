import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox

def submit_text(text):
    # do something with the text input, such as validate the zip code or use it in a calculation
    print(f"You entered: {text}")

# Define a function to create a new window with a plot
def create_new_window():
    fig = plt.figure(figsize=(8, 6))
    # First plot
    ax1 = fig.add_subplot(2, 1, 1)  # 2 rows, 1 column, first plot
    x1 = [1, 2, 3, 4, 5]
    y1 = [25, 16, 9, 4, 1]
    ax1.plot(x1, y1)
   # Create two text boxes
    zip1 = TextBox(plt.axes([0.1, 0.89, 0.25, 0.06]), 'Zip Code 1:')
    zip2 = TextBox(plt.axes([0.6, 0.89, 0.25, 0.06]), 'Zip Code 2:')
    # Set a callback function to be called when the user submits text
    zip1.on_submit(submit_text)
    zip2.on_submit(submit_text)
    # Second plot
    ax2 = fig.add_subplot(2, 1, 2)  # 2 rows, 1 column, second plot
    x2 = [0, 1, 2, 3, 4, 5]
    y2 = [0, 1, 4, 9, 16, 25]
    ax2.plot(x2, y2)
    plt.show()    
