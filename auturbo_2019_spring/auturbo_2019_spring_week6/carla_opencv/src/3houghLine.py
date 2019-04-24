#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage
import math

class Hough():
    def __init__(self):
        self._sub = rospy.Subscriber('/carla/hero/camera/rgb/front/image_color', Image, self.callback, queue_size=1)

        self.bridge = CvBridge()
        
    def callback(self, image_msg):
    	src = self.bridge.imgmsg_to_cv2(image_msg, "bgr8")
    	dst = cv2.Canny(src, 50, 200, None, 3)
    	cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    	cdstP = np.copy(cdst)
    	lines = cv2.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)

    	if lines is not None:
    	    for i in range(0, len(lines)):
	        rho = lines[i][0][0]
	        theta = lines[i][0][1]
	        a = math.cos(theta)
	        b = math.sin(theta)
	        x0 = a * rho
	        y0 = b * rho
	        pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
	        pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
	        cv2.line(cdst, pt1, pt2, (0, 0, 255), 3, cv2.LINE_AA)
	linesP = cv2.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 10)

	if linesP is not None:
	    for i in range(0, len(linesP)):
	        l = linesP[i][0]
	        cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 1, cv2.LINE_AA)
	 
	cv2.imshow("Source", src), cv2.waitKey(1)
	#cv2.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst), cv2.waitKey(1)
	cv2.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP), cv2.waitKey(1)

    def main(self):
        rospy.spin()

if __name__ == '__main__':

    rospy.init_node('Hough')
    node = Hough()
    node.main()
