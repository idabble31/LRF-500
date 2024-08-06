#!/usr/bin/env python3
import matplotlib.pyplot as plt
import pandas as pd

# List of CSV files and their corresponding algorithm names
csv_files = [
    ('data/realworld_data/sesi_2/dynamic/odom/a_star_1.csv', 'A*'),
    ('data/realworld_data/sesi_2/dynamic/odom/dijkstra_1.csv', 'Dijkstra'),
    ('data/realworld_data/sesi_2/dynamic/odom/d_star_lite_1.csv', 'D* Lite'),
    ('data/realworld_data/sesi_2/dynamic/odom/rrt_1.csv', 'RRT'),
    ('data/realworld_data/sesi_2/dynamic/odom/rrt_star_1.csv', 'RRT*'),
    ('data/realworld_data/sesi_2/dynamic/odom/informed_rrt_2.csv', 'Informed RRT')
]

# Define colors for each algorithm
colors = ['red', 'green', 'blue', 'orange', 'magenta','yellow']
# Create the plot and axis objects
fig, ax = plt.subplots()

# Plot the trajectories
for (file, label), color in zip(csv_files, colors):
    data = pd.read_csv(file)
    ax.plot(data['PosX'], data['PosY'], label=label, color=color)

# Add axis labels
ax.set_xlabel('X Position (m)')
ax.set_ylabel('Y Position (m)')

# Title formatting
title = 'Qualitative Comparison\nMap: motion_lab (dynamic)'
title_parts = title.split('\n')
plt.text(0.5, 1.05, title_parts[0], fontsize=16, fontweight='bold', ha='center', transform=ax.transAxes)
plt.text(0.5, 1.01, title_parts[1], fontsize=14, ha='center', transform=ax.transAxes)

# Add legend and grid
ax.legend()
ax.grid()

# Show the plot
plt.show()
