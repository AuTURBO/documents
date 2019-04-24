#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage


class Display_image():
    def __init__(self):
        self.selecting_sub_image = "compressed"

        if self.selecting_sub_image == "compressed":
            self._sub = rospy.Subscriber('/image_compressed', CompressedImage, self.callback, queue_size=1)
        else:
            self._sub = rospy.Subscriber('/image_raw', Image, self.callback, queue_size=1)

        self.bridge = CvBridge()
        
    def callback(self, image_msg):

        if self.selecting_sub_image == "compressed":
            #converting compressed image to opencv image
            np_arr = np.fromstring(image_msg.data, np.uint8)
            cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        elif self.selecting_sub_image == "raw":
            cv_image = self.bridge.imgmsg_to_cv2(image_msg, "bgr8")
        cv2.namedWindow('display_image')
        cv2.moveWindow('display_image', 700,30)
        cv2.imshow('display_image', cv_image), cv2.waitKey(1)

    def main(self):
        rospy.spin()

if __name__ == '__main__':

    rospy.init_node('Display_image')
    node = Display_image()
    node.main()
