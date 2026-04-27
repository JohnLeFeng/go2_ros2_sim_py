import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import xacro

def generate_launch_description():
    # Paths to files and directories
    pkg_path = get_package_share_directory('b2w_description')
    xacro_path = os.path.join(pkg_path, 'xacro', 'robot.xacro')
    
    # Declare launch arguments
    user_debug_arg = DeclareLaunchArgument(
        'user_debug',
        default_value='false',
        description='Enable debug mode'
    )
    robot_name = 'robot1'
    
    # Command to convert xacro to robot_description
    robot_desc = xacro.process_file(xacro_path, mappings={'robot_name': robot_name}).toxml()
    params_robot_state_publisher = {'robot_description': robot_desc, 'use_sim_time': True}

    # Robot state publisher
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params_robot_state_publisher],
    )
    
    # Joint state publisher GUI
    joint_state_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        parameters=[{'use_gui': True}],
        output='screen'
    )

    return LaunchDescription([
        user_debug_arg,
        node_robot_state_publisher,
        joint_state_gui,
    ])
