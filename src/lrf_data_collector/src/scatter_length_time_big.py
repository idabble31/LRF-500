#!/usr/bin/env python3

import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import rospy

class CompareAlgorithms:
    def __init__(self):
        rospy.init_node('compare_algorithms_node', anonymous=True)
        
        self.algorithms = {
            'Dijkstra': ['data/realworld_data/sesi_2/static/odom/dijkstra_1.csv',
                         'data/realworld_data/sesi_2/static/odom/dijkstra_2.csv',
                         'data/realworld_data/sesi_2/static/odom/dijkstra_3.csv'],
            'A*': ['data/realworld_data/sesi_2/static/odom/a_star_1.csv',
                   'data/realworld_data/sesi_2/static/odom/a_star_2.csv',
                   'data/realworld_data/sesi_2/static/odom/a_star_3.csv'],
            'D* Lite': ['data/realworld_data/sesi_2/static/odom/dsl_1.csv',
                        'data/realworld_data/sesi_2/static/odom/dsl_2.csv',
                        'data/realworld_data/sesi_2/static/odom/dsl_3.csv'],
            'RRT': ['data/realworld_data/sesi_2/static/odom/rrt_1.csv',
                    'data/realworld_data/sesi_2/static/odom/rrt_2.csv',
                    'data/realworld_data/sesi_2/static/odom/rrt_3.csv'],
            'RRT*':['data/realworld_data/sesi_2/static/odom/rrt_star_1.csv',
                    'data/realworld_data/sesi_2/static/odom/rrt_star_2.csv',
                    'data/realworld_data/sesi_2/static/odom/rrt_star_3.csv'],
            'Informed RRT':  ['data/realworld_data/sesi_2/static/odom/informed_rrt_1.csv',
                              'data/realworld_data/sesi_2/static/odom/informed_rrt_2.csv',
                              'data/realworld_data/sesi_2/static/odom/informed_rrt_3.csv']
        }
        
        self.compare_algorithms()

    def compare_algorithms(self):
        avg_times = {}
        avg_lengths = {}
        
        for algorithm, files in self.algorithms.items():
            times = []
            lengths = []
            for csv_file in files:
                time, length = self.read_csv_data(csv_file)
                if time is not None and length is not None:
                    times.append(time)
                    lengths.append(length)
            
            if times and lengths:
                avg_times[algorithm] = np.mean(times)
                avg_lengths[algorithm] = np.mean(lengths)
        
        self.print_comparison_table(avg_times, avg_lengths)
        self.plot_comparison(avg_times, avg_lengths)

    def read_csv_data(self, csv_file):
        try:
            with open(csv_file, mode='r') as file:
                reader = csv.DictReader(file)
                times = []
                x_meters = []
                y_meters = []
                
                for row in reader:
                    try:
                        current_time = float(row['Time'])
                        pos_x = float(row['PosX'])
                        pos_y = float(row['PosY'])
                        times.append(current_time)
                        x_meters.append(pos_x)
                        y_meters.append(pos_y)
                    except (ValueError, TypeError) as e:
                        rospy.logwarn(f"Skipping invalid row in {csv_file}: {row}. Error: {e}")
                
                if times and x_meters and y_meters:
                    time_taken = max(times) - min(times)
                    trajectory_length = 0
                    for i in range(1, len(x_meters)):
                        dx = x_meters[i] - x_meters[i - 1]
                        dy = y_meters[i] - y_meters[i - 1]
                        trajectory_length += np.sqrt(dx**2 + dy**2)
                    return time_taken, trajectory_length
        except IOError as e:
            rospy.logerr(f"Failed to read file {csv_file}. Error: {e}")
        return None, None

    def print_comparison_table(self, avg_times, avg_lengths):
        print(f"{'Algorithm':<20} {'Avg Time (s)':<15} {'Avg Trajectory Length (m)':<25}")
        print("="*60)
        for algorithm in avg_times.keys():
            print(f"{algorithm:<20} {avg_times[algorithm]:<15.2f} {avg_lengths[algorithm]:<25.2f}")

    def plot_comparison(self, avg_times, avg_lengths):
        algorithms = list(avg_times.keys())
        times = list(avg_times.values())
        lengths = list(avg_lengths.values())

        markers = ['o', 's', '^', 'D', 'v','>']
        colors = ['b', 'g', 'r', 'c', 'm','y']

        fig, ax = plt.subplots(figsize=(12, 8))

        for i, algorithm in enumerate(algorithms):
            ax.scatter(times[i], lengths[i], label=algorithm, marker=markers[i], color=colors[i], s=100)

        avg_time = np.mean(times)
        avg_length = np.mean(lengths)

        ax.axhline(avg_length, color='gray', linestyle='--')
        ax.axvline(avg_time, color='gray', linestyle='--')

        ax.set_xlabel('Average Time to Reach Goal (s)')
        ax.set_ylabel('Average Trajectory Length (m)')

        # Split title and apply different styles
        title = 'Quantitative Comparison\nMap: motion_lab (static)'
        title_parts = title.split('\n')
        ax.set_title(r'$\bf{' + title_parts[0] + '}$' + '\n' + title_parts[1], fontsize=16)
        ax.legend()

        plt.show()

if __name__ == '__main__':
    try:
        CompareAlgorithms()
    except rospy.ROSInterruptException:
        pass
