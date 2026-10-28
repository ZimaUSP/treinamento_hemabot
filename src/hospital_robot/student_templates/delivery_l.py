"""Missão ROS 2: entrega em um corredor hospitalar em formato de L."""

from enum import Enum, auto

from geometry_msgs.msg import Twist

import rclpy
from rclpy.node import Node


class MissionState(Enum):
    WAITING = auto()
    FIRST_STRAIGHT = auto()
    BEFORE_TURN = auto()
    TURNING = auto()
    SECOND_STRAIGHT = auto()
    DELIVERING = auto()
    FINISHED = auto()


class DeliveryL(Node):
    """Executa uma sequência aberta: reta, curva, reta e entrega."""

    # TODO 1: escolha as velocidades da missão.
    LINEAR_SPEED = 0.0
    ANGULAR_SPEED = 0.0

    WAIT_TIME = 2.0
    FIRST_STRAIGHT_TIME = 10.0
    BEFORE_TURN_TIME = 1.0
    TURN_TIME = 3.1416
    SECOND_STRAIGHT_TIME = 7.5
    DELIVERY_TIME = 5.0

    def __init__(self, node_name='delivery_l'):
        super().__init__(node_name)

        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.state = MissionState.WAITING
        self.state_started_at = self.get_clock().now()
        self.finished_logged = False
        self.timer = self.create_timer(0.05, self.control_loop)

        self.get_logger().info('Missão iniciada: aguardando.')

    def elapsed_in_state(self):
        return (
            self.get_clock().now() - self.state_started_at
        ).nanoseconds / 1e9

    def change_state(self, new_state):
        self.state = new_state
        self.state_started_at = self.get_clock().now()
        self.get_logger().info(f'Novo estado: {new_state.name}')

    def control_loop(self):
        elapsed = self.elapsed_in_state()
        command = Twist()

        if self.state == MissionState.WAITING:
            if elapsed >= self.WAIT_TIME:
                self.change_state(MissionState.FIRST_STRAIGHT)

        elif self.state == MissionState.FIRST_STRAIGHT:
            # TODO 2: comande a primeira reta.
            command.linear.x = 0.0
            if elapsed >= self.FIRST_STRAIGHT_TIME:
                command.linear.x = 0.0
                self.change_state(MissionState.BEFORE_TURN)

        elif self.state == MissionState.BEFORE_TURN:
            if elapsed >= self.BEFORE_TURN_TIME:
                self.change_state(MissionState.TURNING)

        elif self.state == MissionState.TURNING:
            # TODO 3: comande uma curva de 90 graus para a esquerda.
            command.angular.z = 0.0
            if elapsed >= self.TURN_TIME:
                command.angular.z = 0.0
                self.change_state(MissionState.SECOND_STRAIGHT)

        elif self.state == MissionState.SECOND_STRAIGHT:
            # TODO 4: comande a segunda reta.
            command.linear.x = 0.0
            if elapsed >= self.SECOND_STRAIGHT_TIME:
                command.linear.x = 0.0
                self.change_state(MissionState.DELIVERING)

        elif self.state == MissionState.DELIVERING:
            if elapsed >= self.DELIVERY_TIME:
                self.change_state(MissionState.FINISHED)

        elif self.state == MissionState.FINISHED and not self.finished_logged:
            self.get_logger().info('Entrega concluída. Robô parado.')
            self.finished_logged = True

        self.publisher.publish(command)


def main(args=None):
    rclpy.init(args=args)
    node = DeliveryL()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.publisher.publish(Twist())
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
