import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.qos import ReliabilityPolicy
from raspike_uros_msg.msg import SpikeDevStatusMessage


class ImuRecorder(Node):
    def __init__(self):
        super().__init__('imu_recorder')

        self.acc = open('xsens_acc.mat', mode='w')
        self.gyro = open('xsens_gyro.mat', mode='w')

        qos_profile = QoSProfile(depth=4, reliability=ReliabilityPolicy.BEST_EFFORT)

        self.subscription = self.create_subscription(
            SpikeDevStatusMessage, "spike_device_status",
            self.status_on_subscribe, qos_profile)

    def destroy_node(self):
        self.acc.close()
        self.gyro.close()
        super().destroy_node()

    def status_on_subscribe(self, status):
        ts = status.timestamp_usec * 1e-6

        x = status.linear_acceleration[0]
        y = status.linear_acceleration[1]
        z = status.linear_acceleration[2]

        self.acc.write(f'{ts:.9e} {x:.6e} {y:.6e} {z:.6e}\n')
        self.acc.flush()

        x = status.angular_velocity[0]
        y = status.angular_velocity[1]
        z = status.angular_velocity[2]

        self.gyro.write(f'{ts:.9e} {x:.6e} {y:.6e} {z:.6e}\n')
        self.gyro.flush()


def main(args=None):
    rclpy.init(args=args)
    node = ImuRecorder()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
