import math
import sys
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from std_msgs.msg import Float64


class fab_global_position(Node):

    def __init__(self):
        super().__init__('fab_global_position')

        self.wheel_radius = 0.03
        self.wheel_separation = 0.17

        # Declaration DeltaTime Variables
        self.DT = 0.0
        self.CurrentTime = 0.0
        self.PrevTime = 0.0

        # Declaration Robin Transforms Variable
        self.PosX = 0.0
        self.PosY = 0.0
        self.Tetha = 0.0

        # Wheel Velocity Variables
        self.Vel_WL = Float64()
        self.Vel_WR = Float64()

        self.create_subscription(
            Twist,
            '/input_ik',
            self.expensive_calculation_bruh,
            10
        )
        self.create_subscription(
            Float64,
            '/left_wheel/command',
            self.LeftWheelCallback,
            10
        )
        self.create_subscription(
            Float64,
            '/right_wheel/command',
            self.RightWheelCallback,
            10
        )

        #self.create_timer(0.1, self.publish_sheels)

        self.get_logger().info(
            f'Activeeeee'
        )

    def LeftWheelCallback(self, msg):
        self.Vel_WL.data = msg.data
        self.get_logger().info(
            f'Left Wheel Velocity: {self.Vel_WL.data} | Right Wheel Velocity: {self.Vel_WR}'
        )
        

    def RightWheelCallback(self, msg):
        self.Vel_WR.data = msg.data
        self.get_logger().info(
            f'Right Wheel Velocity: {self.Vel_WR.data} | Left Wheel Velocity: {self.Vel_WL}'
        )

    def expensive_calculation_bruh(self, msg):

        self.PrevTime = self.CurrentTime
        self.CurrentTime = self.get_clock().now().nanoseconds * 1e-9
        self.DT = self.CurrentTime - self.PrevTime

        if self.CurrentTime == 0:
            return

        # Bahan Tempur
        # self.Vel = msg.linear.x
        # self.Omega = msg.angular.z

        # Linear Speedddddddd
        ThisLinearSpeed = (self.Vel_WL.data + self.Vel_WR.data) * (self.wheel_radius / 2)
        self.get_logger().info(
            f'[LOGGER] Linear Speed: {ThisLinearSpeed} m/s'
        )
        self.get_logger().info(
            f'[LOGGER] Angular: {msg.angular.z} rad/s'
        )

        ThisXDot = ThisLinearSpeed * math.cos(msg.angular.z)
        ThisYDot = ThisLinearSpeed * math.sin(msg.angular.z)

        self.PosX += ThisXDot * self.DT
        self.PosY += ThisYDot * self.DT
        self.Tetha += msg.angular.z * self.DT

        self.get_logger().info(
            f'[LOGGER] DT: {self.DT}: '
            f'PosX: {self.PosX}, PosY: {self.PosY} '
            f'θ: {self.Tetha}'
        )

def main(args=None):
    rclpy.init(args=args)

    node = fab_global_position()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()