#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32

class MecanumDriveController:
    def __init__(self):
        rospy.init_node('mecanum_drive_controller')
        self.cmd_vel_sub = rospy.Subscriber('cmd_vel', Twist, self.cmd_vel_callback)
        self.fl_pwm_pub = rospy.Publisher('fl_pwm', Int32, queue_size=10)
        self.fr_pwm_pub = rospy.Publisher('fr_pwm', Int32, queue_size=10)
        self.bl_pwm_pub = rospy.Publisher('bl_pwm', Int32, queue_size=10)
        self.br_pwm_pub = rospy.Publisher('br_pwm', Int32, queue_size=10)

    def cmd_vel_callback(self, msg):
        # Extract linear and angular velocities from Twist message
        linear_x = (msg.linear.x*-1)
        linear_y = msg.linear.y
        angular_z = msg.angular.z

        # Calculate wheel velocities for mecanum drive
        fl_velocity = linear_x + linear_y + angular_z
        fr_velocity = (linear_x - linear_y - angular_z)*-1
        bl_velocity = linear_x - linear_y + angular_z
        br_velocity = (linear_x + linear_y - angular_z)*-1

        # Convert wheel velocities to PWM values
        fl_pwm = self.convert_to_pwm(fl_velocity)
        fr_pwm = self.convert_to_pwm(fr_velocity)
        bl_pwm = self.convert_to_pwm(bl_velocity)
        br_pwm = self.convert_to_pwm(br_velocity)

        # Publish PWM values for each wheel
        self.fl_pwm_pub.publish(fl_pwm)
        self.fr_pwm_pub.publish(fr_pwm)
        self.bl_pwm_pub.publish(bl_pwm)
        self.br_pwm_pub.publish(br_pwm)

    def convert_to_pwm(self, velocity):
        # Convert linear velocity to PWM value
        # You need to implement this conversion based on your motor controllers and robot specifications
        # Replace the following line with your implementation
        min_pwm = 0
        max_pwm = 100
        max_velocity = 1.0
        pwm_value = min_pwm + (max_pwm - min_pwm) * (velocity / max_velocity)
        return int(pwm_value)

if __name__ == '__main__':
    try:
        controller = MecanumDriveController()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
