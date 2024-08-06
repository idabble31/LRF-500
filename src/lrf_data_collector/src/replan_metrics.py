#!/usr/bin/env python3

import rospy
import time
import csv
import os
import numpy as np
from nav_msgs.msg import Path

class PathPlannerMetrics:
    def __init__(self):
        self.replanning_count = 0
        self.cumulative_time = 0
        self.total_attempts = 0
        self.successful_replans = 0
        self.previous_path = None
        self.last_replan_time = None
        
        # Ensure the directory exists
        self.csv_path = 'data/realworld_data/sesi_2/static/replan/dsl_3.csv'
        os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)
        
        # Open the CSV file
        self.csv_file = open(self.csv_path, 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['Timestamp', 'Replanning Count', 'Replanning Time', 'Cumulative Replanning Time', 'Path Deviation', 'Success Rate'])
        
        self.plan_sub = rospy.Subscriber('/move_base/GraphPlanner/plan', Path, self.plan_callback)
        rospy.on_shutdown(self.shutdown_hook)
        
        rospy.loginfo("Data collection started. Listening for path updates...")
    
    def plan_callback(self, msg):
        current_time = rospy.get_time()
        timestamp = current_time
        if self.previous_path is not None:
            self.replanning_count += 1
            self.total_attempts += 1
            
            # Calculate replanning time
            replanning_time = current_time - self.last_replan_time
            self.cumulative_time += replanning_time
            
            # Calculate path deviation
            new_path = self.extract_path(msg)
            path_deviation = self.compute_path_deviation(self.previous_path, new_path)
            
            # Assume replanning is always successful for this example
            self.successful_replans += 1
            success_rate = self.successful_replans / self.total_attempts
            
            # Log data to CSV
            self.csv_writer.writerow([timestamp, self.replanning_count, replanning_time, self.cumulative_time, path_deviation, success_rate * 100])
            self.csv_file.flush()  # Ensure data is written to the file
        
        self.previous_path = self.extract_path(msg)
        self.last_replan_time = current_time
    
    def extract_path(self, path_msg):
        return [(pose.pose.position.x, pose.pose.position.y) for pose in path_msg.poses]
    
    def compute_path_deviation(self, original_path, new_path):
        deviation = 0
        min_length = min(len(original_path), len(new_path))
        for orig, new in zip(original_path[:min_length], new_path[:min_length]):
            deviation += np.linalg.norm(np.array(orig) - np.array(new))
        
        # If paths are of different lengths, add the length difference as deviation
        if len(original_path) != len(new_path):
            deviation += abs(len(original_path) - len(new_path))
        
        return deviation
    
    def shutdown_hook(self):
        self.csv_file.close()
        rospy.loginfo("Shutting down and closing CSV file.")
        rospy.loginfo("Data collection finished.")

if __name__ == "__main__":
    rospy.init_node('path_planner_metrics')
    ppm = PathPlannerMetrics()
    rospy.spin()
