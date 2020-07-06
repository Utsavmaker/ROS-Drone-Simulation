#! /usr/bin/env python
import rospy
from geometry_msgs.msg import Twist, PoseStamped
from sensor_msgs.msg import LaserScan

front = 0
n = 0
m = 0


def TakeoffLand():
    global landing, isGoal,twist_msg, cmd_vel_pub, twist_active
    rospy.init_node('takeoff_land') # Creates the node

    twist_msg = Twist() # Twist message to publish for hovering

    # Subcribers
    takeoff_sub = rospy.Subscriber('/ground_truth_to_tf/pose', PoseStamped, takeoff_cb) # Information about pose of the drone
    sub = rospy.Subscriber('/scan', LaserScan, callback)


    # Publishers
    cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1) # For sending z command velocity for takeoff and hover
   
    rate = rospy.Rate(5) # rate at which to revisit callbacks
    rospy.spin() # keeps the node alive

def takeoff_cb(msg):

    global twist_msg, cmd_vel_pub, front, m, n

    ranges = str(front)


    z_pos = msg.pose.position.z
    x = msg.pose.position.x
    y = msg.pose.position.y

    if n < 400 and front >= 2 :
      twist_msg.linear.z = 1.6-z_pos
      cmd_vel_pub.publish(twist_msg)
      rospy.loginfo_once("Drone Takeoff")
    rospy.sleep(0.01)
    n+=1

    if n > 400 and front >= 2 :
	rospy.loginfo_once("Distance Frome The Wall "+ ranges)
	twist_msg.linear.z = 1.6-z_pos
	twist_msg.linear.x = 0.3
	rospy.loginfo_once("Moving Forward")
	cmd_vel_pub.publish(twist_msg)

    if front <= 2:
	twist_msg.linear.z = 1.6-z_pos
	twist_msg.linear.x = 0
	cmd_vel_pub.publish(twist_msg)
	rospy.loginfo_once("Wall Ahead")
	m += 1
	while m > 500:
		rospy.loginfo_once("Landing Start")
		twist_msg.linear.z = -0.3
		cmd_vel_pub.publish(twist_msg)
		m += 1
		while m > 700:
			rospy.loginfo_once("DRONE HAS LANDED. System is shutting down. Stopping drone...")
			rospy.signal_shutdown("DRONE HAS LANDED")
			
	

def callback(msg):
    global front
    front = msg.ranges[540]

if __name__ == '__main__':
    TakeoffLand()
