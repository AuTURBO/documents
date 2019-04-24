#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage

class Gray():
    def __init__(self):
        self.selecting_sub_image = "raw" # you can choose image type "compressed", "raw"

        if self.selecting_sub_image == "compressed":
            self._sub = rospy.Subscriber('/image_compressed', CompressedImage, self.callback, queue_size=1)
        else:
            self._sub = rospy.Subscriber('/image_raw', Image, self.callback, queue_size=1)

        self.bridge = CvBridge()
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    def callback(self, image_msg):

        if self.selecting_sub_image == "compressed":
            #converting compressed image to opencv image
            np_arr = np.fromstring(image_msg.data, np.uint8)
            cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        elif self.selecting_sub_image == "raw":
            cv_image = self.bridge.imgmsg_to_cv2(image_msg, "bgr8")

        cv_gray = cv2.cvtColor(cv_image, cv2.COLOR_RGB2GRAY)
        faces = self.face_cascade.detectMultiScale(cv_gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(cv_image,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = cv_gray[y:y+h, x:x+w]
            roi_color = cv_image[y:y+h, x:x+w]
            eyes = self.eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

        cv2.imshow('cv_image', cv_image), cv2.waitKey(1)
    def main(self):
        rospy.spin()

if __name__ == '__main__':
    rospy.init_node('gray')
    node = Gray()
    node.main()
