#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage


class Hough():
    def __init__(self):
        self._sub = rospy.Subscriber('/carla/hero/camera/rgb/front/image_color', Image, self.callback, queue_size=1)

        self.bridge = CvBridge()
        
    def callback(self, image_msg):
        cv_image = self.bridge.imgmsg_to_cv2(image_msg, "bgr8")

        gray = cv2.cvtColor(cv_image,cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray,50,150,apertureSize = 3)
        minLineLength = 100
        maxLineGap = 10
        lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)

        for x1,y1,x2,y2 in lines[0]:
            cv2.line(cv_image,(x1,y1),(x2,y2),(0,255,0),2)



        cv2.imshow('hough', cv_image), cv2.waitKey(1)
        cv2.imshow('edge', edges), cv2.waitKey(1)

    def main(self):
        rospy.spin()

if __name__ == '__main__':

    rospy.init_node('Hough')
    node = Hough()
    node.main()
