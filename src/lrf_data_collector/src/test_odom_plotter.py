#!/usr/bin/env python3

import csv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import yaml

class PlotOdomOnMap:
    def __init__(self):
        self.csv_file = 'data/realworld_data/test/odom/test_odom8.csv'
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

        x, y = [], []
        with open(self.csv_file, mode='r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    pos_x = float(row['PosX'])
                    pos_y = float(row['PosY'])
                    x.append((pos_x - origin[0]) / resolution)
                    y.append((pos_y - origin[1]) / resolution)
                except (ValueError, TypeError) as e:
                    print(f"Skipping invalid row: {row}. Error: {e}")
                    continue

        if not x or not y:
            print(f"No valid odometry data found in {self.csv_file}.")
            return

        # Invert the y-axis
        y = [img.shape[0] - yi for yi in y]

        # Convert x and y to meters
        x_meters = [xi * resolution for xi in x]
        y_meters = [yi * resolution for yi in y]

        ax.plot(x_meters, y_meters, color='blue', linewidth=1, label='Odometry Path')

        ax.set_title('Odometry Path on Map')
        ax.set_xlabel('x in [m]')
        ax.set_ylabel('y in [m]')
        ax.legend()
        plt.show()

if __name__ == '__main__':
    PlotOdomOnMap()
