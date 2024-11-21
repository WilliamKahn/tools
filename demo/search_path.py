import matplotlib.pyplot as plt
import numpy as np

# Create a 5x5 grid
grid_size = 5
colors = np.full((grid_size, grid_size), 'blue')

fig, ax = plt.subplots()
ax.set_xticks(np.arange(0.5, grid_size, 1))
ax.set_yticks(np.arange(0.5, grid_size, 1))
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.grid(True)

# Create a scatter plot for the grid
x, y = np.meshgrid(np.arange(grid_size), np.arange(grid_size))
sc = ax.scatter(x, y, c=colors.flatten(), s=500, marker='s')

def on_click(event):
    if event.inaxes == ax:
        col = int(event.xdata)
        row = int(event.ydata)
        if 0 <= col < grid_size and 0 <= row < grid_size:
            index = row * grid_size + col
            colors[row, col] = 'red' if colors[row, col] == 'blue' else 'blue'
            sc.set_color(colors.flatten())
            fig.canvas.draw()

fig.canvas.mpl_connect('button_press_event', on_click)
plt.show()