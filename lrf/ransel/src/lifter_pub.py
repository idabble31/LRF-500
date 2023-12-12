#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from pynput import keyboard

def on_press(key):
    try:
        key_str = key.char
        publish_keyboard_input(key_str)
    except AttributeError:
        pass

def on_release(key):
    if key == keyboard.Key.esc:
        return False  # Stop listener

def publish_keyboard_input(key_str):
    key_msg = String()
    key_msg.data = key_str
    key_publisher.publish(key_msg)

if __name__ == '__main__':
    rospy.init_node('keyboard_publisher', anonymous=True)
    key_publisher = rospy.Publisher('keyboard_input', String, queue_size=10)  # Update with your desired topic name

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        rospy.spin()
