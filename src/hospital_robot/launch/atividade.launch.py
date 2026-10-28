"""Inicia o Gazebo Harmonic e a ponte de tópicos com ROS 2 Jazzy."""

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.actions import OpaqueFunction
from launch.actions import SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node


def _launch_setup(context):
    package_dir = get_package_share_directory('hospital_robot')
    ros_gz_sim_dir = get_package_share_directory('ros_gz_sim')
    models_dir = os.path.join(package_dir, 'models')

    world_name = LaunchConfiguration('world').perform(context)
    if not world_name.endswith('.sdf'):
        world_name += '.sdf'

    allowed_worlds = {
        'introduction.sdf',
        'hospital_l.sdf',
        'hospital_l_challenge.sdf',
    }
    if world_name not in allowed_worlds:
        raise RuntimeError(
            f'Mundo desconhecido: {world_name}. '
            f'Opções: {sorted(allowed_worlds)}'
        )

    world_path = os.path.join(package_dir, 'worlds', world_name)
    headless = LaunchConfiguration('headless').perform(context).lower()
    server_only = headless in {'1', 'true', 'yes'}
    gz_args = f'-r -v 3 {"-s " if server_only else ""}"{world_path}"'

    resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=os.pathsep.join(filter(None, [
            models_dir,
            os.environ.get('GZ_SIM_RESOURCE_PATH', ''),
        ])),
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_dir, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={
            'gz_args': gz_args,
            'on_exit_shutdown': 'true',
        }.items(),
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
        ],
        output='screen',
    )

    return [resource_path, gazebo, bridge]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'world',
            default_value='hospital_l',
            description=(
                'Mundo: introduction, hospital_l ou hospital_l_challenge.'
            ),
        ),
        DeclareLaunchArgument(
            'headless',
            default_value='false',
            description='Executa somente o servidor do Gazebo, sem interface.',
        ),
        OpaqueFunction(function=_launch_setup),
    ])
