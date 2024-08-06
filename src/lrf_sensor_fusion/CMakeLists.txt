cmake_minimum_required(VERSION 3.0.2)
project(lrf_sensor_fusion)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  nav_msgs
  sensor_msgs
  tf
  robot_localization
)

catkin_package()

include_directories(
  ${catkin_INCLUDE_DIRS}
)
