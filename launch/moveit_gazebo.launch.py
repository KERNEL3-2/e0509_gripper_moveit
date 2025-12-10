import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
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

    # Move Group Node - Gazebo controller에 연결
    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            moveit_config.to_dict(),
            {"use_sim_time": True},
        ],
        remappings=[
            ("/joint_states", "/e0509_gripper/joint_states"),
            ("follow_joint_trajectory", "/e0509_gripper/joint_trajectory_controller/follow_joint_trajectory"),
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
        name="rviz2",
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

    # Robot State Publisher
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="both",
        parameters=[
            moveit_config.robot_description,
            {"use_sim_time": True},
        ],
        remappings=[
            ("/joint_states", "/e0509_gripper/joint_states"),
        ],
    )

    return LaunchDescription([
        robot_state_publisher,
        move_group_node,
        rviz_node,
    ])
