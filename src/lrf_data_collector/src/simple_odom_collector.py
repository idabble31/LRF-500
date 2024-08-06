#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Odometry
import csv
import os

class OdomToCSV:
    def __init__(self):
        rospy.init_node('odom_to_csv_node', anonymous=True)
        
        # Subscriber
        self.odom_sub = rospy.Subscriber('/camera/odom/sample', Odometry, self.odom_callback)
        
        # CSV file setup
        self.csv_file = 'data/realworld_data/sesi_2/static/odom/dsl_3.csv'
        self.init_csv()
        
        # Data storage
        self.odom_data = []
        
        # Set up signal handler for graceful shutdown
        rospy.on_shutdown(self.shutdown_hook)
        
        rospy.loginfo("Data collection started.")

    def init_csv(self):
        os.makedirs(os.path.dirname(self.csv_file), exist_ok=True)
        with open(self.csv_file, mode='w') as file:
            writer = csv.writer(file)
            writer.writerow(['Time', 'PosX', 'PosY', 'PosZ', 'OriX', 'OriY', 'OriZ', 'OriW'])

    def odom_callback(self, msg):
        timestamp = msg.header.stamp.to_sec()
        position = msg.pose.pose.position
        orientation = msg.pose.pose.orientation
        self.odom_data.append([timestamp, position.x, position.y, position.z,
                               orientation.x, orientation.y, orientation.z, orientation.w])
        # Debugging print statement
        rospy.loginfo(f"Received odometry: Time={timestamp}, Pos=({position.x}, {position.y}, {position.z}), "
                      f"Ori=({orientation.x}, {orientation.y}, {orientation.z}, {orientation.w})")

    def save_csv(self):
        with open(self.csv_file, mode='a') as file:
            writer = csv.writer(file)
            writer.writerows(self.odom_data)

    def shutdown_hook(self):
        rospy.loginfo("Shutting down and saving collected data.")
        self.save_csv()
        rospy.loginfo("Data collection finished. CSV file closed.")

if __name__ == '__main__':
    try:
        OdomToCSV()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
