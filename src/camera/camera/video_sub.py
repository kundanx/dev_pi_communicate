import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class VideoSubscriber(Node):
    def __init__(self):
        super().__init__('video_subscriber')
        self.image_subscription = self.create_subscription(
            Image,
            'camera_image',  # Replace with the actual topic name
            self.image_callback,
            10  # Adjust the queue size as needed
        )
        self.bridge = CvBridge()

    def image_callback(self, msg):
        # Convert ROS image message to OpenCV image
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        # Display or process the video frame as needed
        cv2.imshow('Video Stream', cv_image)
        cv2.waitKey(1)  # Adjust the wait time as needed

def main(args=None):
    rclpy.init(args=args)
    video_subscriber = VideoSubscriber()
    rclpy.spin(video_subscriber)
    video_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()