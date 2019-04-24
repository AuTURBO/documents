#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage


class Publisher():
    def __init__(self):
        self._pub1 = rospy.Publisher('/image_compressed', CompressedImage, queue_size=1)
        self._pub2 = rospy.Publisher('/image_raw', Image, queue_size=1)

        self.bridge = CvBridge()


    def main(self):
        print('start')
        cam = cv2.VideoCapture(0)
        cv2.namedWindow('publisher')
        cv2.moveWindow('publisher', 40,30)
        while True:
            ret_val, cv_image = cam.read()
            #publising compressed image
            msg_raw_image = CompressedImage()
            msg_raw_image.header.stamp = rospy.Time.now()
            msg_raw_image.format = "jpeg"
            msg_raw_image.data = np.array(cv2.imencode('.jpg', cv_image)[1]).tostring()
            self._pub1.publish(msg_raw_image)

            #publishing raw image
            self._pub2.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
            cv2.imshow('publisher', cv_image)
            key = cv2.waitKey(20) & 0xFF
            if key!=255:
                break
        cam.release 
        cv2.destroyAllWindows() 
        exit()
if __name__ == '__main__':
    rospy.init_node('publisher')
    node = Publisher()
    node.main()
