#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32

class DiffDriveController:
    def __init__(self):
        rospy.init_node('differential_controller')
        self.cmd_vel_sub = rospy.Subscriber('cmd_vel', Twist, self.cmd_vel_callback)
        self.pwm_fl_pub = rospy.Publisher('fl_pwm', Int32, queue_size=10)
        self.pwm_fr_pub = rospy.Publisher('fr_pwm', Int32, queue_size=10)
        self.pwm_bl_pub = rospy.Publisher('bl_pwm', Int32, queue_size=10)
        self.pwm_br_pub = rospy.Publisher('br_pwm', Int32, queue_size=10)# Initialize other variables as needed

    def cmd_vel_callback(self, msg):
        # Extract linear and angular velocities
        linear_x = msg.linear.x
        angular_z = msg.angular.z

        # Calculate wheel velocities based on linear and angular velocities
        v = linear_x
        omega = angular_z

        # Calculate left and right wheel velocities
        v_left = (v - (omega * R))*-1
        v_right = v + (omega * R)

        # Convert wheel velocities to PWM values
        pwm_left = self.convert_to_pwm(v_left)
        pwm_right = self.convert_to_pwm(v_right)

        # Publish PWM values to control the motors
        self.pwm_fl_pub.publish(pwm_left)
        self.pwm_fr_pub.publish(pwm_right)
        self.pwm_bl_pub.publish(pwm_left)
        self.pwm_br_pub.publish(pwm_right)

    def convert_to_pwm(self, velocity):
        # Convert linear velocity to PWM value
        # You need to implement this conversion based on your motor controllers and robot specifications
        # Replace the following line with your implementation
        min_pwm = 0
        max_pwm = 150
        max_velocity = 1.0
        pwm_value = min_pwm + (max_pwm - min_pwm) * (velocity/max_velocity)
        return int(pwm_value)

if __name__ == '__main__':
    try:
        R = 0.2281  # Example value for the wheelbase (distance from center to wheel)
        conversion_factor = 1.0  # Example conversion factor from velocity to PWM value
        controller = DiffDriveController()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
