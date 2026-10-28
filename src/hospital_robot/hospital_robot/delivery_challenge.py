"""Desafio ROS 2: interrompe a segunda reta diante de um obstáculo."""

import math

from geometry_msgs.msg import Twist

from hospital_robot.delivery_l import DeliveryL, MissionState

import rclpy

from sensor_msgs.msg import LaserScan


class DeliveryChallenge(DeliveryL):
    """Acrescenta uma parada de segurança baseada no LiDAR."""

    STOP_DISTANCE = 0.50
    SLOW_DISTANCE = 0.80
    FRONT_HALF_ANGLE_DEGREES = 15.0

    def __init__(self):
        super().__init__('delivery_challenge')
        self.front_distance = math.inf
        self.blocked_since = None
        self.scan_subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10,
        )
        self.get_logger().info('Desafio com LiDAR ativado.')

    def scan_callback(self, scan):
        half_angle = math.radians(self.FRONT_HALF_ANGLE_DEGREES)
        valid_ranges = []

        for index, distance in enumerate(scan.ranges):
            angle = scan.angle_min + index * scan.angle_increment
            if abs(angle) <= half_angle and math.isfinite(distance):
                if scan.range_min <= distance <= scan.range_max:
                    valid_ranges.append(distance)

        self.front_distance = min(valid_ranges, default=math.inf)

    def control_loop(self):
        if self.state != MissionState.SECOND_STRAIGHT:
            self.blocked_since = None
            super().control_loop()
            return

        command = Twist()

        if self.front_distance < self.STOP_DISTANCE:
            if self.blocked_since is None:
                self.blocked_since = self.get_clock().now()
                self.get_logger().warn(
                    'Obstáculo próximo: robô parado por segurança.'
                )
            self.publisher.publish(command)
            return

        if self.blocked_since is not None:
            blocked_duration = self.get_clock().now() - self.blocked_since
            self.state_started_at = self.state_started_at + blocked_duration
            self.blocked_since = None
            self.get_logger().info('Caminho liberado: retomando a missão.')

        elapsed = self.elapsed_in_state()
        command.linear.x = self.LINEAR_SPEED

        if self.front_distance < self.SLOW_DISTANCE:
            command.linear.x *= 0.35

        if elapsed >= self.SECOND_STRAIGHT_TIME:
            command.linear.x = 0.0
            self.change_state(MissionState.DELIVERING)

        self.publisher.publish(command)


def main(args=None):
    rclpy.init(args=args)
    node = DeliveryChallenge()

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
