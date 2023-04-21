import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox

monthly_dni = None
monthly_ghi = None

gs = plt.GridSpec(nrows=7, ncols=1, figure=None)

rect1 = None
rect2 = None

variables = {'zipcode': None, 'surfaceArea': None, 'powerRating': None, 'efficiency': None, 'cost': None, 'time': None}

def submit(text, variable):
    variables[variable] = float(text)
    print(variable, ':', variables[variable])

# Captures the input values from the textboxes and updates the corrseponding values in the variables array
# The on_submit method uses an anonymous function to choose which value to update

# Zip code
axbox = plt.subplot(gs[1, 0])
zipcode_box = TextBox(axbox, "Zip Code", textalignment="center")
zipcode_box.on_submit(lambda text: submit(text, 'zipcode'))

# Surface area
axbox = plt.subplot(gs[2, 0])
area_box = TextBox(axbox, "Surface Area", textalignment="center")
area_box.on_submit(lambda text: submit(text, 'surfaceArea'))

# Power rating
axbox = plt.subplot(gs[3, 0])
power_box = TextBox(axbox, "Power Rating", textalignment="center")
power_box.on_submit(lambda text: submit(text, 'powerRating'))

# Efficency
axbox = plt.subplot(gs[4, 0])
efficency_box = TextBox(axbox, "Efficency", textalignment="center")
efficency_box.on_submit(lambda text: submit(text, 'efficency'))

# Cost
axbox = plt.subplot(gs[5, 0])
cost_box = TextBox(axbox, "Cost", textalignment="center")
cost_box.on_submit(lambda text: submit(text, 'cost'))

# Time
axbox = plt.subplot(gs[6, 0])
time_box = TextBox(axbox, "Time", textalignment="center")
time_box.on_submit(lambda text: submit(text, 'time'))

plt.subplots_adjust(wspace=0.2, hspace=0.1)

#redraw()
plt.show()