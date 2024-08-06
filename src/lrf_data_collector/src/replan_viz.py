#!/usr/bin/env python3

import rospy
import pandas as pd
import matplotlib.pyplot as plt

class PathPlannerVisualizer:
    def __init__(self):
        rospy.init_node('path_planner_visualizer')

        # List of CSV files to compare
        self.csv_files = [
            'data/realworld_data/sesi_2/dynamic/replan/d_star_lite_1.csv',
            'data/realworld_data/sesi_2/dynamic/replan/a_star_1.csv',
            'data/realworld_data/sesi_2/dynamic/replan/dijkstra_1.csv',
            'data/realworld_data/sesi_2/dynamic/replan/rrt_1.csv',
            'data/realworld_data/sesi_2/dynamic/replan/rrt_star_1.csv',
            'data/realworld_data/sesi_2/dynamic/replan/informed_rrt_1.csv'
        ]
        
        self.labels = ['D*Lite', 'A*', 'Dijkstra', 'RRT', 'RRT*', 'Informed RRT']
        self.colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown']
        self.dataframes = []

        for file in self.csv_files:
            try:
                df = pd.read_csv(file)
                if 'Timestamp' not in df.columns:
                    rospy.logwarn(f"'Timestamp' column not found in {file}. Available columns: {df.columns.tolist()}")
                self.dataframes.append(df)
            except Exception as e:
                rospy.logerr(f"Failed to read {file}: {e}")
        
        self.visualize_metrics()

    def visualize_metrics(self):
        fig, axs = plt.subplots(1, 2, figsize=(14, 7))  # Adjusted to 1 row and 2 columns

        # Replanning Count Bar Chart
        replanning_counts = [df['Replanning Count'].sum() for df in self.dataframes]
        bars1 = axs[0].bar(range(len(self.labels)), replanning_counts, color=self.colors)
        axs[0].set_xlabel('Algorithms')
        axs[0].set_ylabel('Total Replanning Count')
        axs[0].set_title('Replanning Count Comparison')
        axs[0].set_xticks(range(len(self.labels)))
        axs[0].set_xticklabels(self.labels)  # Show x-tick labels

        # Cumulative Replanning Time Bar Chart
        cumulative_replanning_times = [df['Cumulative Replanning Time'].iloc[-1] for df in self.dataframes]
        bars2 = axs[1].bar(range(len(self.labels)), cumulative_replanning_times, color=self.colors)
        axs[1].set_xlabel('Algorithms')
        axs[1].set_ylabel('Total Cumulative Replanning Time (s)')
        axs[1].set_title('Cumulative Replanning Time Comparison')
        axs[1].set_xticks(range(len(self.labels)))
        axs[1].set_xticklabels(self.labels)  # Show x-tick labels

        # Add the overall title
        plt.suptitle(r'$\bf{Replanning\ Performance\ Comparison}$' + '\nMap: motion_lab (dynamic)', fontsize=16)

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()

if __name__ == "__main__":
    visualizer = PathPlannerVisualizer()
    rospy.spin()
