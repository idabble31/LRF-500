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
        self.csv_file = 'data/realworld_data/test/odom/dsl.csv'
        self.map_file = rospy.get_param('~map_file', 'lab_fisika.pgm')
        self.map_yaml = rospy.get_param('~map_yaml', 'lab_fisika.yaml') 
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

        fig, ax = plt.subplots()
        ax.imshow(img, origin='lower', cmap='gray', extent=[0, img.shape[1] * resolution, 0, img.shape[0] * resolution])

        with open(self.csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            x = []
            y = []
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
            rospy.logerr("No valid odometry data found. Exiting.")
            return

        # Invert the y-axis
        y = [img.shape[0] - yi for yi in y]

        # Convert x and y to meters
        x_meters = [xi * resolution for xi in x]
        y_meters = [yi * resolution for yi in y]

        # Calculate the length of the trajectory
        trajectory_length = 0
        for i in range(1, len(x_meters)):
            dx = x_meters[i] - x_meters[i - 1]
            dy = y_meters[i] - y_meters[i - 1]
            trajectory_length += np.sqrt(dx**2 + dy**2)

        ax.plot(x_meters, y_meters, marker='o', markersize=2, linestyle='-', color='green', label='Trajectory')

        # Plot the start and goal positions
        if x_meters and y_meters:
            start_position = (x_meters[0], y_meters[0])
            goal_position = (x_meters[-1], y_meters[-1])
            ax.scatter(start_position[0], start_position[1], c='yellow', marker='o', s=100, label='Start')
            ax.scatter(goal_position[0], goal_position[1], c='blue', marker='*', s=100, label='Goal')

        # Optional: Plot obstacles (uncomment if needed)
        # obstacle_x = [15, 16, 17]
        # obstacle_y = [8.5, 8.5, 8.5]
        # ax.scatter(obstacle_x, obstacle_y, c='red', marker='x', s=100, label='Obstacle')

        ax.set_title(f'basic physics lab Map (A*)\nTrajectory Length: {trajectory_length:.2f} meters')
        ax.set_xlabel('X (meters)')
        ax.set_ylabel('Y (meters)')
        ax.legend()
        plt.show()

if __name__ == '__main__':
    try:
        PlotOdomOnMap()
    except rospy.ROSInterruptException:
        pass
