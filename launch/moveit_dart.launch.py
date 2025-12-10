import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():
    
    moveit_config = (
        MoveItConfigsBuilder("e0509_with_gripper", package_name="e0509_gripper_moveit_config")
        .robot_description(file_path="config/e0509_gripper.urdf")
        .robot_description_semantic(file_path="config/dsr.srdf")
        .robot_description_kinematics(file_path="config/kinematics.yaml")
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .to_moveit_configs()
    )

    # Move Group Node
    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            moveit_config.to_dict(),
            {"use_sim_time": True},
        ],
        remappings=[
            ("/joint_states", "/dsr01/joint_states"),
        ],
    )

    # RViz
    rviz_config = os.path.join(
        get_package_share_directory("e0509_gripper_moveit_config"), 
        "launch", "moveit.rviz"
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2_moveit",
        output="log",
        arguments=["-d", rviz_config],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.planning_pipelines,
            moveit_config.robot_description_kinematics,
            {"use_sim_time": True},
        ],
    )

    return LaunchDescription([
        move_group_node,
        rviz_node,
    ])
