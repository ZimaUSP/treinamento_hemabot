"""Demonstração completa: Gazebo, ponte ROS 2 e missão."""

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.actions import TimerAction
from launch.conditions import IfCondition
from launch.conditions import UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node


def generate_launch_description():
    package_dir = get_package_share_directory('hospital_robot')
    world = LaunchConfiguration('world')
    headless = LaunchConfiguration('headless')
    challenge = LaunchConfiguration('challenge')

    activity = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(package_dir, 'launch', 'atividade.launch.py')
        ),
        launch_arguments={
            'world': world,
            'headless': headless,
        }.items(),
    )

    normal_mission = Node(
        package='hospital_robot',
        executable='entrega_programada',
        parameters=[{'use_sim_time': True}],
        output='screen',
        condition=UnlessCondition(challenge),
    )

    challenge_mission = Node(
        package='hospital_robot',
        executable='delivery_challenge',
        parameters=[{'use_sim_time': True}],
        output='screen',
        condition=IfCondition(challenge),
    )

    delayed_mission = TimerAction(
        period=3.0,
        actions=[normal_mission, challenge_mission],
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'world',
            default_value='hospital_l',
            description='Mundo a carregar.',
        ),
        DeclareLaunchArgument(
            'headless',
            default_value='false',
            description='Executa o Gazebo sem interface.',
        ),
        DeclareLaunchArgument(
            'challenge',
            default_value='false',
            description='Executa o controlador com segurança por LiDAR.',
        ),
        activity,
        delayed_mission,
    ])
