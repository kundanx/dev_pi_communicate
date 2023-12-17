import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Float32MultiArray
from cv_bridge import CvBridge
import cv2

from ultralytics import YOLO
import supervision as sv
import numpy as np
import math
import pdb


fx = (1.445*10**3)/2
fy = (1.430*10**3)/2

cx = (567.369)/2
cy = (342.353)/2

k1 = -0.0202
k2 = 1.1829
k3 = -3.9788

p1 = -0.0113
p2 = -0.0040

intrinsic_matrix = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])
distortion_coeffs = np.array([k1, k2, p1, p2, k3])

def get_center(bbox):
    length  = (bbox[2] - bbox[0])
    breadth = (bbox[3] - bbox[1])

    x = bbox[0] + (length/2)
    y = bbox[1] + (breadth/2)

    return int(x), int(y)

    
def get_angle(ball_center, intrinsic_matrix) -> int:
    '''
    Get the angle of vector pointing to the detected ball_center
    '''
    fx = intrinsic_matrix[0, 0]
    fy = intrinsic_matrix[1, 1]
    f = int((fx+fy)/2)
    x_center = ball_center[0]
    y_center = ball_center[0]
    x_principal = intrinsic_matrix[0,2]
    y_principal = intrinsic_matrix[1,2]

    theta = round(math.degrees(math.atan((x_center-x_principal)/f)))
    return theta


class ObjectTracker(Node):
    def __init__(self):
        super().__init__('object_tracker')
        self.image_subscription = self.create_subscription(
            Image,
            'camera_image',  
            self.image_callback,
            5 
        )
        self.publisher = self.create_publisher(Float32MultiArray, '/ball_pos_topic', 5)
        self.undistort_pub = self.create_publisher(Image, 'undistort_image', 5)
        self.tracked_pub = self.create_publisher(Image, 'tracked_image', 5)
        
        # import pdb; pdb.set_trace()
        self.bridge = CvBridge()
        self.model = '/home/apil/Club/Robotics/yolov8/turtlebot/src/camera/camera/best_new.pt'
        self.model = YOLO(self.model)
        self.box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=1,
        text_scale=0.5
        )
    def image_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        self.track_ball(cv_image)     

    
    def track_ball(self, frame):
        # model = YOLO(self.model)
        frame = cv2.undistort(frame, intrinsic_matrix, distortion_coeffs)
        undistort_frame = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        self.undistort_pub.publish(undistort_frame)
        results = self.model.track(source=frame, persist=True)
        ball_pos = Float32MultiArray()
        for result in results:
            detections = sv.Detections.from_yolov8(result)
            theta = {}
        
            if result.boxes.id is not None:
                detections.tracker_id = result.boxes.id.cpu().numpy().astype(int)

                for item in range(len(detections.xyxy)):
                    x_center, y_center = get_center(detections.xyxy[item])

                    theta[detections.tracker_id[item]] = get_angle(intrinsic_matrix=intrinsic_matrix, ball_center=(x_center, y_center))
                    ball_pos.data.append(theta[detections.tracker_id[item]])
                    ball_pos.data.append((detections.xyxy[item][3]-detections.xyxy[item][1])/2)
 
                labels = [
                f"#{tracker_id} {confidence:.2f} {theta[tracker_id]}"
                for _, confidence, _, tracker_id
                in detections
                ]
                frame = self.box_annotator.annotate(scene=frame, detections=detections, labels=labels)

            else:
                ball_pos.data = [-1.0, -1.0]
        # ball_pos.data = [0.1,0.5]
        tracked_frame = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        self.tracked_pub.publish(tracked_frame)
        self.publisher.publish(ball_pos)

def main(args=None):
    rclpy.init(args=args)
    object_tracker = ObjectTracker()
    rclpy.spin(object_tracker)
    object_tracker.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()