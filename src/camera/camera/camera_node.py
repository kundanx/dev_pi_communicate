import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class CameraNode(Node):
    def __init__(self):
        super().__init__('camera_node')
        self.image_publisher = self.create_publisher(Image, 'camera_image', 10)
        self.timer = self.create_timer(0.033, self.publish_image)  # Adjust the timer rate as needed
        self.bridge = CvBridge()

        # OpenCV video capture (adjust the video source or file path as needed)
        self.cap = cv2.VideoCapture(0)

    def publish_image(self):
        # Capture video frame
        ret, frame = self.cap.read()

        if ret:
            # Convert OpenCV image to ROS image message
            ros_image_msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')

            # Publish the image message
            self.image_publisher.publish(ros_image_msg)

def main(args=None):
    rclpy.init(args=args)
    camera_node = CameraNode()
    rclpy.spin(camera_node)
    camera_node.destroy_node()
    rclpy.shutdown()

# if __name__ == '__camera_node__':
#     main()
