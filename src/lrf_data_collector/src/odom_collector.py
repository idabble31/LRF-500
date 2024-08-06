#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseStamped
import rosgraph_msgs.msg
import csv
import os
import numpy as np
import signal
import sys

class OdomToCSV:
    def __init__(self):
        rospy.init_node('odom_to_csv_node', anonymous=True)
        
        # Subscribers
        self.odom_sub = rospy.Subscriber('/camera/odom/sample', Odometry, self.odom_callback)
        self.log_sub = rospy.Subscriber('/rosout', rosgraph_msgs.msg.Log, self.log_callback)
        
        # Initial pose and goal publishers
        self.initial_pose_pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size=10)
        self.goal_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
        
        # CSV file setup
        self.csv_file = 'data/realworld_data/test/odom/test_odom8.csv'
        self.init_csv()
        
        self.start_time = rospy.Time.now()
        self.odom_data = []
        
        # Set up signal handler for graceful shutdown
        rospy.on_shutdown(self.shutdown_hook)
        
        rospy.loginfo("Data collection started immediately.")

    def init_csv(self):
        os.makedirs(os.path.dirname(self.csv_file), exist_ok=True)
        with open(self.csv_file, mode='w') as file:
            writer = csv.writer(file)
            writer.writerow(['Time', 'PosX', 'PosY', 'PosZ', 'OriX', 'OriY', 'OriZ', 'OriW'])

    def odom_callback(self, msg):
        current_time = rospy.Time.now().to_sec()
        position = msg.pose.pose.position
        orientation = msg.pose.pose.orientation
        self.odom_data.append([current_time, position.x, position.y, position.z,
                               orientation.x, orientation.y, orientation.z, orientation.w])

    def log_callback(self, msg):
        if "Goal reached" in msg.msg:
            self.goal_reached()

    def goal_reached(self):
        end_time = rospy.Time.now()
        duration = (end_time - self.start_time).to_sec()
        rospy.loginfo(f"Goal reached! Time taken: {duration} seconds.")
        self.start_time = rospy.Time.now()  # Reset start time for next goal

        self.save_csv()
        trajectory_length = self.calculate_trajectory_length()
        rospy.loginfo(f"Trajectory length: {trajectory_length:.2f} meters.")
        
        # Append time taken and trajectory length to the CSV
        with open(self.csv_file, mode='a') as file:
            writer = csv.writer(file)
            writer.writerow([])
            writer.writerow(['Time taken (s)', duration])
            writer.writerow(['Trajectory length (m)', trajectory_length])

    def save_csv(self):
        with open(self.csv_file, mode='a') as file:
            writer = csv.writer(file)
            writer.writerows(self.odom_data)
        self.odom_data = []  # Clear data after saving

    def calculate_trajectory_length(self):
        trajectory_length = 0
        for i in range(1, len(self.odom_data)):
            dx = self.odom_data[i][1] - self.odom_data[i-1][1]
            dy = self.odom_data[i][2] - self.odom_data[i-1][2]
            trajectory_length += np.sqrt(dx**2 + dy**2)
        return trajectory_length

    def shutdown_hook(self):
        rospy.loginfo("Shutting down and processing collected data.")
        if self.odom_data:
            self.goal_reached()  # Process data if any
        else:
            rospy.loginfo("No data collected.")
        rospy.loginfo("Data collection finished. Closing CSV file.")

if __name__ == '__main__':
    try:
        OdomToCSV()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
