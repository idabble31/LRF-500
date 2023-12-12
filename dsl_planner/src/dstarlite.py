#!/usr/bin/env python3

from nav_core.base_global_planner import BaseGlobalPlanner
from pluginlib import SimplePlugin
import rospy
from nav_msgs.msg import OccupancyGrid, Path
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
import heapq
import math

class DStarLiteROS(BaseGlobalPlanner, SimplePlugin):
    def __init__(self):
        rospy.init_node('dstar_lite_planner')
        
        # Subscribers
        rospy.Subscriber('/map', OccupancyGrid, self.map_callback)
        rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, self.pose_callback)
        rospy.Subscriber('/move_base_simple/goal', PoseStamped, self.goal_callback)
        
        # Publishers
        self.path_pub = rospy.Publisher('/dstar_lite_path', Path, queue_size=1)
        
        # Initialize variables
        self.start = None
        self.goal = None
        self.km = 0
        self.graph = {}
        self.U = []

    def map_callback(self, msg):
        if not self.start or not self.goal:
            # Initialize only once when both start and goal are available
            return
        
        width = msg.info.width
        height = msg.info.height
        data = msg.data

        self.graph = {}
        for i in range(width):
            for j in range(height):
                index = j * width + i
                cost = data[index]
                self.graph[(i, j)] = cost

        self.U = [(self.calculate_key(self.start), self.start)]
        self.compute_shortest_path()

    def pose_callback(self, pose_msg):
        # Update start position based on AMCL pose estimate
        self.start = (int(pose_msg.pose.pose.position.x), int(pose_msg.pose.pose.position.y))
        if self.goal:
            self.map_callback(None)  # Trigger map update

    def goal_callback(self, goal_msg):
        # Update goal position when a new goal is received
        self.goal = (int(goal_msg.pose.position.x), int(goal_msg.pose.position.y))
        self.compute_shortest_path()

    def calculate_key(self, node):
        return (min(self.g(node), self.rhs(node)) + self.heuristic(node, self.start) + self.km, min(self.g(node), self.rhs(node)))

    def heuristic(self, a, b):
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

    def g(self, node):
        return self.graph.get(node, float('inf'))

    def rhs(self, node):
        if node == self.goal:
            return 0
        return self.graph.get(node, float('inf'))

    def update_vertex(self, node):
        if node != self.start:
            self.graph[node] = min(self.g(node), self.rhs(node))

        if node in self.U:
            self.U.remove(node)
            heapq.heapify(self.U)

        if self.g(node) != self.rhs(node):
            heapq.heappush(self.U, (self.calculate_key(node), node))

    def compute_shortest_path(self):
        if not self.start or not self.goal:
            # Wait until both start and goal are available
            return

        while self.U and (self.U[0][0] < self.calculate_key(self.goal) or self.rhs(self.goal) != self.g(self.goal)):
            k_old, u = heapq.heappop(self.U)

            if k_old < self.calculate_key(u):
                heapq.heappush(self.U, (self.calculate_key(u), u))
            elif self.g(u) > self.rhs(u):
                self.graph[u] = self.rhs(u)
                for succ in self.get_neighbors(u):
                    self.update_vertex(succ)
            else:
                self.graph[u] = float('inf')
                for succ in self.get_neighbors(u) + [u]:
                    self.update_vertex(succ)

        self.publish_path()

    def get_neighbors(self, node):
        x, y = node
        neighbors = []
        for i in range(max(0, x-1), min(width, x+2)):
            for j in range(max(0, y-1), min(height, y+2)):
                if (i, j) != node:
                    neighbors.append((i, j))
        return neighbors

    def publish_path(self):
        path_msg = Path()
        path_msg.header.stamp = rospy.Time.now()
        path_msg.header.frame_id = "map"

        current = self.start
        while current != self.goal:
            pose = PoseStamped()
            pose.pose.position.x = current[0]
            pose.pose.position.y = current[1]
            path_msg.poses.append(pose)

            neighbors = self.get_neighbors(current)
            best_neighbor = min(neighbors, key=lambda n: self.g(n) + self.heuristic(n, self.start))
            current = best_neighbor

        self.path_pub.publish(path_msg)

    def replan(self):
        self.km += self.heuristic(self.start, self.goal)
        self.compute_shortest_path()

if __name__ == '__main__':
    dstar_ros = DStarLiteROS()
    rospy.spin()
