#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage




def callback(x):
    pass

class Mask():
    def __init__(self):
        self.selecting_sub_image = "raw" # you can choose image type "compressed", "raw"

        if self.selecting_sub_image == "compressed":
            self._sub = rospy.Subscriber('/image_compressed', CompressedImage, self.callback, queue_size=1)
        else:
            self._sub = rospy.Subscriber('/image_raw', Image, self.callback, queue_size=1)

        self.bridge = CvBridge()

    def callback(self, image_msg):

        H_low = 0
        H_high = 180
        S_low = 0
        S_high = 255
        V_low = 0
        V_high = 255

        # creating trackbar
        cv2.namedWindow('cv_result')
        cv2.createTrackbar('H_low','cv_result',H_low, 180,callback)
        cv2.createTrackbar('H_high','cv_result',H_high, 180,callback)
        cv2.createTrackbar('S_low','cv_result',S_low, 255,callback)
        cv2.createTrackbar('S_high','cv_result',S_high, 255,callback)
        cv2.createTrackbar('V_low','cv_result',V_low, 255,callback)
        #cv2.createTrackbar('V_high','cv_result',V_high, 255,callback)

        # getting homography variables from trackbar
        H_low = cv2.getTrackbarPos('H_low', 'cv_result')
        H_high = cv2.getTrackbarPos('H_high', 'cv_result')
        S_low = cv2.getTrackbarPos('S_low', 'cv_result')
        S_high = cv2.getTrackbarPos('S_high', 'cv_result')
        V_low = cv2.getTrackbarPos('V_low', 'cv_result')
        #V_high = cv2.getTrackbarPos('V_high', 'cv_result')

        HSV_low = np.array([H_low, S_low, V_low])
        HSV_high = np.array([H_high, S_high, V_high])

        if self.selecting_sub_image == "compressed":
            #converting compressed image to opencv image
            np_arr = np.fromstring(image_msg.data, np.uint8)
            cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        elif self.selecting_sub_image == "raw":
            cv_image = self.bridge.imgmsg_to_cv2(image_msg, "bgr8")

        cv_hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        cv_mask = cv2.inRange(cv_hsv, HSV_low, HSV_high)
        cv_result = cv2.bitwise_and(cv_image, cv_image, mask=cv_mask)

        params=cv2.SimpleBlobDetector_Params()
        # Change thresholds
        params.minThreshold = 0
        params.maxThreshold = 255

        # Filter by Area.
        params.filterByArea = True
        params.minArea = 700
        params.maxArea = 10000

        # Filter by Circularity
        params.filterByCircularity = True
        params.minCircularity = 0.1

        # Filter by Convexity
        params.filterByConvexity = True
        params.minConvexity = 0.3



        det=cv2.SimpleBlobDetector_create(params)
        keypts=det.detect(~cv_mask)
        cv_image=cv2.drawKeypoints(cv_image,keypts,np.array([]),(0,255,255),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        cv2.imshow('cv_image', cv_image), cv2.waitKey(1)
        cv2.imshow('cv_mask', cv_mask), cv2.waitKey(1)
        cv2.imshow('cv_result', cv_result), cv2.waitKey(1)
    def main(self):
        rospy.spin()

if __name__ == '__main__':
    rospy.init_node('mask')
    node = Mask()
    node.main()
