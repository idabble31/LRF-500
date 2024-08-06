#!/usr/bin/env python3

import rospy
import csv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import yaml
import os
import numpy as np

class PlotOdomOnMap:
    def __init__(self):
        rospy.init_node('plot_odom_on_map_node', anonymous=True)
        self.csv_files = {
            'Dijkstra': ['data/realworld_data/dynamic/odom/dijkstra_1.csv',
                         'data/realworld_data/dynamic/odom/dijkstra_2.csv',
                         'data/realworld_data/dynamic/odom/dijkstra_3.csv'],
            'A*': ['data/realworld_data/dynamic/odom/a_star_1.csv',
                   'data/realworld_data/dynamic/odom/a_star_2.csv',
                   'data/realworld_data/dynamic/odom/a_star_3.csv'],
            'D* Lite': ['data/realworld_data/dynamic/odom/d_star_lite_1.csv',
                        'data/realworld_data/dynamic/odom/d_star_lite_2.csv',
                        'data/realworld_data/dynamic/odom/d_star_lite_3.csv'],
            'RRT': ['data/realworld_data/dynamic/odom/rrt_1.csv',
                    'data/realworld_data/dynamic/odom/rrt_2.csv',
                    'data/realworld_data/dynamic/odom/rrt_3.csv'],
            'RRT*':['data/realworld_data/dynamic/odom/rrt_star_1.csv',
                    'data/realworld_data/dynamic/odom/rrt_star_2.csv',
                    'data/realworld_data/dynamic/odom/rrt_star_3.csv'],
            'Informed RRT':  ['data/realworld_data/dynamic/odom/informed_rrt_1.csv',
                              'data/realworld_data/dynamic/odom/informed_rrt_2.csv',
                              'data/realworld_data/dynamic/odom/informed_rrt_3.csv']
        }
        self.map_file = 'lab_fisika.pgm'
        self.map_yaml = 'lab_fisika.yaml'
        self.plot_odom_on_map()

    def read_map_info(self):
        with open(self.map_yaml, 'r') as file:
            map_info = yaml.safe_load(file)
        return map_info

    def plot_odom_on_map(self):
        map_info = self.read_map_info()
        img = mpimg.imread(self.map_file)

        # Map parameters
        resolution = map_info['resolution']
        origin = map_info['origin']

        fig, ax = plt.subplots(figsize=(10, 8))
        ax.imshow(img, origin='lower', cmap='gray', extent=[0, img.shape[1] * resolution, 0, img.shape[0] * resolution])

        colors = ['red', 'green', 'blue', 'orange', 'magenta','yellow']
        markers = ['o', 's', '^', 'D', '*','+']

        for i, (algorithm, files) in enumerate(self.csv_files.items()):
            for j, file in enumerate(files):
                x, y = [], []
                with open(file, mode='r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        try:
                            pos_x = float(row['PosX'])
                            pos_y = float(row['PosY'])
                            x.append((pos_x - origin[0]) / resolution)
                            y.append((pos_y - origin[1]) / resolution)
                        except (ValueError, TypeError) as e:
                            rospy.logwarn(f"Skipping invalid row: {row}. Error: {e}")
                            continue

                if not x or not y:
                    rospy.logerr(f"No valid odometry data found in {file}.")
                    continue

                # Invert the y-axis
                y = [img.shape[0] - yi for yi in y]

                # Convert x and y to meters
                x_meters = [xi * resolution for xi in x]
                y_meters = [yi * resolution for yi in y]

                ax.plot(x_meters, y_meters, color=colors[i], linewidth=1, label=f'({algorithm})' if j == 0 else "")
                
                #if j == 0:
                #    # Plot a single start and goal position for each algorithm
                #    start_position = (x_meters[0], y_meters[0])
                #    goal_position = (x_meters[-1], y_meters[-1])
                #    ax.scatter(*start_position, c='yellow', marker=markers[i], s=100, edgecolors='black', label=f'Start ({algorithm})')
                #    ax.scatter(*goal_position, c='purple', marker='*', s=150, edgecolors='black', label=f'Goal ({algorithm})')

        #start_x = [20.75]
        #start_y =[12.47]
        #goal_x =[2.47]
        #goal_y = [20.65]
        #ax.scatter(start_x, start_y, c='limegreen', marker='v', s=200, label='Start')
        #ax.scatter(goal_x, goal_y, c='firebrick', marker='*', s=200, label='Goal')

        # Title formatting
        title = 'Qualitative Comparison\nMap: basic_physics_lab (static)'
        title_parts = title.split('\n')
        ax.set_title('')
        plt.text(0.5, 1.05, title_parts[0], fontsize=16, fontweight='bold', ha='center', transform=ax.transAxes)
        plt.text(0.5, 1.01, title_parts[1], fontsize=14, ha='center', transform=ax.transAxes)

        ax.set_xlabel('x in [m]')
        ax.set_ylabel('y in [m]')
        ax.legend()
        plt.show()

if __name__ == '__main__':
    try:
        PlotOdomOnMap()
    except rospy.ROSInterruptException:
        pass
