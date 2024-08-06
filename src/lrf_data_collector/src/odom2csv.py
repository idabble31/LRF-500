#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Odometry
import csv
import os

class OdomToCSV:
    def __init__(self):
        rospy.init_node('odom_to_csv_node', anonymous=True)
        self.odom_sub = rospy.Subscriber('/odom', Odometry, self.odom_callback) 
        self.csv_file = 'data/realworld_data/dynamic/odom/a_star.csv'
        self.init_csv()
        print("Retrieving odometry data...")

    def init_csv(self):
        with open(self.csv_file, mode='w') as file:
            writer = csv.writer(file)
            writer.writerow(['Time', 'PosX', 'PosY', 'PosZ', 'OriX', 'OriY', 'OriZ', 'OriW'])

    def odom_callback(self, msg):
        with open(self.csv_file, mode='a') as file:
            writer = csv.writer(file)
            current_time = rospy.Time.now().to_sec()
            position = msg.pose.pose.position
            orientation = msg.pose.pose.orientation
            writer.writerow([current_time, position.x, position.y, position.z,
                             orientation.x, orientation.y, orientation.z, orientation.w])

if __name__ == '__main__':
    try:
        OdomToCSV()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

