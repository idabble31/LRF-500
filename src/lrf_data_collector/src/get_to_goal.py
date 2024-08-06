#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseStamped

def set_initial_pose_and_goal():
    rospy.init_node('set_initial_pose_and_goal')

    # Publisher for initial pose
    initial_pose_pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size=10)

    # Publisher for goal
    goal_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)

    # Allow time for publisher to register
    rospy.sleep(1)

    # Define the initial pose
    initial_pose = PoseWithCovarianceStamped()
    initial_pose.header.stamp = rospy.Time.now()
    initial_pose.header.frame_id = 'map'  # Make sure this matches your map frame
    initial_pose.pose.pose.position.x = 3.6521902084350586
    initial_pose.pose.pose.position.y = 2.2864532470703125
    initial_pose.pose.pose.position.z = 0.0
    initial_pose.pose.pose.orientation.x = 0.0
    initial_pose.pose.pose.orientation.y = 0.0
    initial_pose.pose.pose.orientation.z = -0.6499281159883098
    initial_pose.pose.pose.orientation.w = 0.7599956868613703
    initial_pose.pose.covariance = [0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06853892326654787]

    # Define the goal pose
    goal_pose = PoseStamped()
    goal_pose.header.stamp = rospy.Time.now()
    goal_pose.header.frame_id = 'map'  # Make sure this matches your map frame
    goal_pose.pose.position.x = 1.1583185195922852
    goal_pose.pose.position.y = -2.278761625289917
    goal_pose.pose.position.z = 0.0
    goal_pose.pose.orientation.x = 0.0
    goal_pose.pose.orientation.y = 0.0
    goal_pose.pose.orientation.z = -0.6172110598278379
    goal_pose.pose.orientation.w = 0.7867976281269519

    # Publish the initial pose
    rospy.loginfo("Setting initial pose...")
    initial_pose_pub.publish(initial_pose)
    rospy.sleep(1)  # Allow some time for the initial pose to be set

    # Publish the goal pose
    rospy.loginfo("Sending goal pose...")
    goal_pub.publish(goal_pose)

    rospy.loginfo("Initial pose and goal pose have been set.")

if __name__ == '__main__':
    try:
        set_initial_pose_and_goal()
    except rospy.ROSInterruptException:
        pass
