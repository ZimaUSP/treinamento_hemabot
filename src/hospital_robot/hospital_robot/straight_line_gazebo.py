"""Movimento retilíneo usando somente o transporte nativo do Gazebo."""

import shutil
import subprocess
from threading import Timer


TOPIC = '/cmd_vel'
SPEED = 0.20
MOVE_TIME = 5.0


def publish_velocity(linear_x=0.0, angular_z=0.0):
    """Publica uma única mensagem Twist no transporte do Gazebo."""
    message = (
        f'linear: {{x: {linear_x}}}, '
        f'angular: {{z: {angular_z}}}'
    )
    subprocess.run(
        [
            'gz',
            'topic',
            '-t',
            TOPIC,
            '-m',
            'gz.msgs.Twist',
            '-p',
            message,
        ],
        check=True,
    )


def main():
    if shutil.which('gz') is None:
        raise SystemExit(
            'Comando "gz" não encontrado. Instale o Gazebo Harmonic.'
        )

    print('Enviando movimento retilíneo sem ROS 2...')
    stop_timer = Timer(MOVE_TIME, publish_velocity)
    stop_timer.start()
    try:
        publish_velocity(linear_x=SPEED)
        stop_timer.join()
    finally:
        if stop_timer.is_alive():
            stop_timer.cancel()
        publish_velocity()
        print('Robô parado.')


if __name__ == '__main__':
    main()
