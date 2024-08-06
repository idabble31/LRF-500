#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32
import math

class HolonomicDriveController:
    def __init__(self):
        rospy.init_node('holonomic_controller')
        self.cmd_vel_sub = rospy.Subscriber('cmd_vel', Twist, self.cmd_vel_callback)
        self.pwm_fl_pub = rospy.Publisher('fl_pwm', Int32, queue_size=10)
        self.pwm_fr_pub = rospy.Publisher('fr_pwm', Int32, queue_size=10)
        self.pwm_bl_pub = rospy.Publisher('bl_pwm', Int32, queue_size=10)
        self.pwm_br_pub = rospy.Publisher('br_pwm', Int32, queue_size=10)
        # Initialize other variables as needed

    def cmd_vel_callback(self, msg):
        # Extract linear and angular velocities
        linear_x = msg.linear.x
        linear_y = msg.linear.y
        angular_z = msg.angular.z
        theta = math.radians(45)

        # Calculate wheel velocities based on linear and angular velocities
        v_x= linear_x
        v_y= linear_y
        omega = angular_z
        

        # Calculate left and right wheel velocities
        v_fl = (v_x * math.cos(theta) + v_y * math.sin(theta) + omega * R)*-1
        v_fr = v_x * math.cos(theta) - v_y * math.sin(theta) + omega * R
        v_bl = (v_x * math.cos(theta) - v_y * math.sin(theta) + omega * R)*-1
        v_br = v_x * math.cos(theta) + v_y * math.sin(theta) + omega * R

        # Convert wheel velocities to PWM values
        pwm_fl= self.convert_to_pwm(v_fl)
        pwm_fr= self.convert_to_pwm(v_fr)
        pwm_bl= self.convert_to_pwm(v_bl)
        pwm_br = self.convert_to_pwm(v_br)

        # Publish PWM values to control the motors
        self.pwm_fl_pub.publish(pwm_fl)
        self.pwm_fr_pub.publish(pwm_fr)
        self.pwm_bl_pub.publish(pwm_bl)
        self.pwm_br_pub.publish(pwm_br)

    def convert_to_pwm(self, velocity):
        # Convert linear velocity to PWM value
        # You need to implement this conversion based on your motor controllers and robot specifications
        # Replace the following line with your implementation
        min_pwm = 0
        max_pwm = 255
        max_velocity = 1.0
        pwm_value = min_pwm + (max_pwm - min_pwm) * (velocity/max_velocity)
        return int(pwm_value)

if __name__ == '__main__':
    try:
        R = 0.2281  # Example value for the wheelbase (distance from center to wheel)
        #conversion_factor = 1.0  # Example conversion factor from velocity to PWM value
        controller = HolonomicDriveController()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
