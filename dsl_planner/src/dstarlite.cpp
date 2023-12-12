#include <ros/ros.h>
#include <nav_msgs/OccupancyGrid.h>
#include <nav_msgs/Path.h>
#include <geometry_msgs/PoseStamped.h>
#include <geometry_msgs/PoseWithCovarianceStamped.h>
#include <queue>
#include <cmath>

class DStarLiteROS {
public:
    DStarLiteROS() {
        ros::NodeHandle nh;
        
        // Subscribers
        map_sub = nh.subscribe("/map", 1, &DStarLiteROS::mapCallback, this);
        pose_sub = nh.subscribe("/amcl_pose", 1, &DStarLiteROS::poseCallback, this);
        goal_sub = nh.subscribe("/move_base_simple/goal", 1, &DStarLiteROS::goalCallback, this);
        
        // Publishers
        path_pub = nh.advertise<nav_msgs::Path>("/dstar_lite_path", 1);
        
        // Initialize variables
        start = std::make_pair(-1, -1);
        goal = std::make_pair(-1, -1);
        km = 0;
    }

    void mapCallback(const nav_msgs::OccupancyGrid::ConstPtr& msg) {
        if (start.first == -1 || start.second == -1 || goal.first == -1 || goal.second == -1) {
            // Initialize only once when both start and goal are available
            return;
        }
        
        int width = msg->info.width;
        int height = msg->info.height;

        graph.clear();
        for (int i = 0; i < width; ++i) {
            for (int j = 0; j < height; ++j) {
                int index = j * width + i;
                int cost = msg->data[index];
                graph[std::make_pair(i, j)] = cost;
            }
        }

        U.push(std::make_pair(calculateKey(start), start));
        computeShortestPath();
    }

    void poseCallback(const geometry_msgs::PoseWithCovarianceStamped::ConstPtr& pose_msg) {
        // Update start position based on AMCL pose estimate
        start.first = static_cast<int>(pose_msg->pose.pose.position.x);
        start.second = static_cast<int>(pose_msg->pose.pose.position.y);

        if (goal.first != -1 && goal.second != -1) {
            mapCallback(nullptr);  // Trigger map update
        }
    }

    void goalCallback(const geometry_msgs::PoseStamped::ConstPtr& goal_msg) {
        // Update goal position when a new goal is received
        goal.first = static_cast<int>(goal_msg->pose.position.x);
        goal.second = static_cast<int>(goal_msg->pose.position.y);
        computeShortestPath();
    }

    double calculateKey(const std::pair<int, int>& node) {
        return (std::min(g(node), rhs(node)) + heuristic(node, start) + km, std::min(g(node), rhs(node)));
    }

    double heuristic(const std::pair<int, int>& a, const std::pair<int, int>& b) {
        return std::sqrt(std::pow(a.first - b.first, 2) + std::pow(a.second - b.second, 2));
    }

    double g(const std::pair<int, int>& node) {
        auto it = graph.find(node);
        return (it != graph.end()) ? it->second : std::numeric_limits<double>::infinity();
    }

    double rhs(const std::pair<int, int>& node) {
        return (node == goal) ? 0 : g(node);
    }

    void updateVertex(const std::pair<int, int>& node) {
        if (node != start) {
            graph[node] = std::min(g(node), rhs(node));
        }

        if (U.count(node) > 0) {
            U.erase(node);
        }

        if (g(node) != rhs(node)) {
            U.insert(std::make_pair(calculateKey(node), node));
        }
    }

    void computeShortestPath() {
        if (start.first == -1 || start.second == -1 || goal.first == -1 || goal.second == -1) {
            // Wait until both start and goal are available
            return;
        }

        while (!U.empty() && (U.begin()->first < calculateKey(goal) || rhs(goal) != g(goal))) {
            auto k_old_u = *U.begin();
            U.erase(U.begin());
            double k_old = k_old_u.first;
            auto u = k_old_u.second;

            if (k_old < calculateKey(u)) {
                U.insert(std::make_pair(calculateKey(u), u));
            } else if (g(u) > rhs(u)) {
                graph[u] = rhs(u);
                for (auto& succ : getNeighbors(u)) {
                    updateVertex(succ);
                }
            } else {
                graph[u] = std::numeric_limits<double>::infinity();
                for (auto& succ : getNeighbors(u)) {
                    updateVertex(succ);
                }
                updateVertex(u);
            }
        }

        publishPath();
    }

    std::vector<std::pair<int, int>> getNeighbors(const std::pair<int, int>& node) {
        int x = node.first;
        int y = node.second;
        std::vector<std::pair<int, int>> neighbors;

        for (int i = std::max(0, x - 1); i < std::min(width, x + 2); ++i) {
            for (int j = std::max(0, y - 1); j < std::min(height, y + 2); ++j) {
                if (std::make_pair(i, j) != node) {
                    neighbors.push_back(std::make_pair(i, j));
                }
            }
        }

        return neighbors;
    }

    void publishPath() {
        nav_msgs::Path path_msg;
        path_msg.header.stamp = ros::Time::now();
        path_msg.header.frame_id = "map";

        auto current = start;
        while (current != goal) {
            geometry_msgs::PoseStamped pose;
            pose.pose.position.x = current.first;
            pose.pose.position.y = current.second;
            path_msg.poses.push_back(pose);

            auto neighbors = getNeighbors(current);
            auto best_neighbor = *std::min_element(neighbors.begin(), neighbors.end(),
                [&](const auto& n1, const auto& n2) {
                    return g(n1) + heuristic(n1, start) < g(n2) + heuristic(n2, start);
                });
            current = best_neighbor;
        }

        path_pub.publish(path_msg);
    }

private:
    ros::Subscriber map_sub;
    ros::Subscriber pose_sub;
    ros::Subscriber goal_sub;
    ros::Publisher path_pub;

    std::pair<int, int> start;
    std::pair<int, int> goal;
    double km;
    std::map<std::pair<int, int>, double> graph;
    std::set<std::pair<double, std::pair<int, int>>> U;

    int width;
    int height;
};

int main(int argc, char** argv) {
    ros::init(argc, argv, "dstar_lite_planner_cpp");
    DStarLiteROS dstar_ros;
    ros::spin();
    return 0;
}
