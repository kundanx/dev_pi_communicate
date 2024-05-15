import sys

from robot_localization.srv import SetPose
import rclpy
from rclpy.node import Node


class SetPoseAsyncClient(Node):

    def __init__(self):
        super().__init__('SetPoseAsyncClient')
        self.cli = self.create_client(SetPose, 'set_pose')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = SetPose.Request()

    def send_request(self):
        self.req.pose.header.frame_id = "map"
        self.req.pose.header.stamp = self.get_clock().now().to_msg()

        self.req.pose.pose.pose.position.x = 0.0
        self.req.pose.pose.pose.position.y = 0.0
        self.req.pose.pose.pose.position.z = 0.0

        self.req.pose.pose.covariance = [1e-9, 0.0,  0.0,  0.0,  0.0,  0.0,
                                        0.0,   1e-9, 0.0,  0.0,  0.0,  0.0,
                                        0.0,   0.0,  1e-9, 0.0,  0.0,  0.0,
                                        0.0,   0.0,  0.0,  1e-9, 0.0,  0.0,
                                        0.0,   0.0,  0.0,  0.0,  1e-9, 0.0,
                                        0.0,   0.0,  0.0,  0.0,  0.0,  1e-9]


        
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()


def main():
    rclpy.init()

    set_poseclient = SetPoseAsyncClient()
    set_poseclient.send_request()
    set_poseclient.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()