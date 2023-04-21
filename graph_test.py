import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
import numpy as np

# Generate some example data
x = np.linspace(0, 10, 100)
y3 = np.tan(x)

# Define a function that will be called whenever the user changes the text in a text box
def submit(text):
    print(text)

# Create a GridSpec with two rows and two columns
gs = plt.GridSpec(nrows=2, ncols=2, figure=None)

# Create a subplot for the first graph that spans the entire first row
ax1 = plt.subplot(gs[0, :])
ax1.plot(x, y3)
ax1.set_title('Graph 3')

# Create input text boxes for the second and third rows
ax2 = plt.subplot(gs[1, 0])
text_box1 = TextBox(ax2, '', initial='Enter text here')
text_box1.on_submit(submit)

ax3 = plt.subplot(gs[1, 1])
text_box2 = TextBox(ax3, '', initial='Enter text here')
text_box2.on_submit(submit)

# Adjust the spacing between the subplots
plt.subplots_adjust(wspace=0.3, hspace=0.5)

# Show the figure
plt.show()
