#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage
import math

def center(points):
    center_x = (points[0][0][0] + points[1][0][0] + points[2][0][0] + points[3][0][0])/4.0
    center_y = (points[0][0][1] + points[1][0][1] + points[2][0][1] + points[3][0][1])/4.0
    return center_x, center_y


def find_position(points):
    center_x, center_y = center(points)
    index = np.zeros(4)
    existance0 = 'no'
    existance1 = 'no'
    existance2 = 'no'
    existance3 = 'no'
    existanceall = 'no'
    for i in range(4):
        if points[i][0][0] < center_x:
            if points[i][0][1] > center_y:
                index[3] = i
                existance3 = 'yes'
            else:
                index[0] = i
                existance0 = 'yes'
        else:
            if points[i][0][1] > center_y:
                index[2] = i
                existance2 = 'yes'
            else:
                index[1] = i
                existance1 = 'yes'

    if existance0 == 'yes' and existance1 == 'yes' and existance2 == 'yes' and existance3 == 'yes':
        existanceall = 'yes'
    return existanceall, index


def find_angle(point1, point0, point2):
    y1 = point1[1] - point0[1]
    y2 = point2[1] - point0[1]
    x1 = point1[0] - point0[0]
    x2 = point2[0] - point0[0]
    angle = math.atan2(y1*x2 - x1*y2, x1*x2+y1*y2)*180/np.pi
    return abs(angle)

def distinguish_rectangular(screenCnt):
    threshold_angle = 20
    existance, index = find_position(screenCnt)
    for i in range(4):
        if find_angle(screenCnt[(i+0)%4][0], screenCnt[(i+1)%4][0], screenCnt[(i+2)%4][0]) > 90 + threshold_angle or find_angle(screenCnt[(i+0)%4][0], screenCnt[(i+1)%4][0], screenCnt[(i+2)%4][0]) < 90 - threshold_angle:
            satisfaction_angle = 'no'
            break
        satisfaction_angle = 'yes'
    if satisfaction_angle == 'yes' and existance == 'yes':
        return 'yes'


class Homography():
    def __init__(self):
        self.selecting_sub_image = "raw"

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


        # converting to gray
        cv_gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        # adding blur
        cv_smoothing = cv2.bilateralFilter(cv_gray, 5, 5, 5)
        # findign edge
        cv_edged = cv2.Canny(cv_smoothing, 20, 100)
        # making egde to be thicker
        kernel = np.ones((5,5),np.uint8)
        cv_dilation = cv2.dilate(cv_edged,kernel,iterations = 1)
        #finding contours
        _, cnts, hierarchy = cv2.findContours(cv_dilation.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
        screenCnt = None
        area_pre = 100000


        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            # do this process if contour have 4 edge
            if len(approx) == 4:
                screenCnt = approx
                area_now = cv2.contourArea(c)
                check_rectangular = distinguish_rectangular(screenCnt)
                # do this process if all angles of rectangular between 70 and 110
                if check_rectangular == 'yes' and area_pre - area_now < 10000:
                    cv2.drawContours(cv_image, [screenCnt], -1, (0, 255, 0), 3) # drawing rectangular box
                    for j in range(4):  # drawing circles in vertex
                        cv_image = cv2.circle(cv_image, (screenCnt[j][0][0], screenCnt[j][0][1]), 2, (0, 0, 255), thickness=3, lineType=8, shift=0)
                    _, index = find_position(screenCnt)

                    # Homography processing to make flat image
                    point1 = screenCnt[int(index[0])][0]
                    point2 = screenCnt[int(index[1])][0]
                    point3 = screenCnt[int(index[2])][0]
                    point4 = screenCnt[int(index[3])][0]

                    pts_src = np.array([point1, point2, point3, point4])
                    pts_dst = np.array([[0, 0], [149, 0], [149, 149], [0, 149]])
                    h, status = cv2.findHomography(pts_src, pts_dst)
                    cv_Homography = cv2.warpPerspective(cv_image, h, (150, 150))
                    cv2.imshow("image_Homography", cv_Homography), cv2.waitKey(1)

                area_pre = area_now

        # showing images
        cv2.imshow("image_edged", cv_edged), cv2.waitKey(1)
        cv2.imshow("image_dilation", cv_dilation), cv2.waitKey(1)
        cv2.imshow("image", cv_image), cv2.waitKey(1)


    def main(self):
        rospy.spin()

if __name__ == '__main__':
    rospy.init_node('homography')
    node = Homography()
    node.main()
