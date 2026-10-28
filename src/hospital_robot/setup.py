from glob import glob
import os

from setuptools import find_packages, setup


package_name = 'hospital_robot'


setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name],
        ),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.sdf')),
        (
            os.path.join('share', package_name, 'models', 'hospital_robot'),
            glob('models/hospital_robot/*'),
        ),
        (
            os.path.join('share', package_name, 'student_templates'),
            glob('student_templates/*.py'),
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Equipe de Robótica Hospitalar',
    maintainer_email='robotica@example.com',
    description=(
        'Treinamento introdutório de ROS 2, Gazebo e Python com um '
        'robô móvel em um hospital simulado.'
    ),
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            (
                'straight_line_gazebo = '
                'hospital_robot.straight_line_gazebo:main'
            ),
            'delivery_l = hospital_robot.delivery_l:main',
            'entrega_programada = hospital_robot.delivery_l:main',
            (
                'delivery_challenge = '
                'hospital_robot.delivery_challenge:main'
            ),
        ],
    },
)
