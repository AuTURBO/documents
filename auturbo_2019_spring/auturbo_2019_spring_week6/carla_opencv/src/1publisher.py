#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage


class Publisher():
    def __init__(self):
        self._sub = rospy.Subscriber('/carla/hero/camera/rgb/front/image_color', Image, self.callback, queue_size=1)
        self._pub1 = rospy.Publisher('/image_compressed', CompressedImage, queue_size=1)
        self.bridge = CvBridge()
        
    def callback(self, image_msg):
        cv_image = self.bridge.imgmsg_to_cv2(image_msg, "bgr8")
        #publising compressed image
        msg_cmpressed_image = CompressedImage()
        msg_cmpressed_image.header.stamp = rospy.Time.now()
        msg_cmpressed_image.format = "jpeg"
        msg_cmpressed_image.data = np.array(cv2.imencode('.jpg', cv_image)[1]).tostring()
        self._pub1.publish(msg_cmpressed_image)
       
    def main(self):
        rospy.spin()

if __name__ == '__main__':
    rospy.init_node('publisher')
    node = Publisher()
    node.main()
