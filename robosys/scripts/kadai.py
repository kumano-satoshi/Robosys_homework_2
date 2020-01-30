#!/usr/bin/env python 
#-*- coding:utf-8 -*-

import numpy as np
import rospy
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist


class Robosys(object):
    def __init__(self):
        #---image_sub---
        self.img_sub = rospy.Subscriber("/usb_cam/image_raw", Image, self.cv_callback)
        self.bridge = CvBridge()
        #---kernel_size & HSV---
        self.kernel = np.array((30, 30), np.uint8)
     
        self.blue_lower = np.array([106, 34, 33])
        self.blue_upper = np.array([119, 255, 255])
        self.red1_lower = np.array([176, 107, 0])
        self.red1_upper = np.array([180, 255, 255])
        self.red2_lower = np.array([0, 29, 29])
        self.red2_upper = np.array([1, 255, 255])
        self.green_lower = np.array([28, 39, 0])
        self.green_upper = np.array([96, 255, 255])
     
        #---turtle---
        self.turtle_pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size = "1")


    def mask_f(self, img, lower, upper):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask_pre = cv2.inRange(hsv, lower, upper)
        mask_img = cv2.bitwise_and(img, img, mask = mask_pre)
        return mask_img


    def noise_removal_f(self, img_color):
        img_color = cv2.GaussianBlur(img_color, (33, 33), 1)
        gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
        binarization = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        morphology_close = cv2.morphologyEx(binarization, cv2.MORPH_CLOSE, self.kernel)
        morphology_open = cv2.morphologyEx(morphology_close, cv2.MORPH_OPEN, self.kernel)
        noise_removal = cv2.GaussianBlur(morphology_open, (33, 33), 1)
        return noise_removal


    def area_measurement_f(self, noise_removal):
        image, contour, hierarchy = cv2.findContours(noise_removal, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        area = np.zeros((len(contour), 1))
        try:
            for k in xrange(len(contour)):
                area[k] = cv2.contourArea(contour[k])
                #print(area[k])
            area_max = max(area)
        except:
            area_max = 0
            print("nothing")
        return area_max


    def cv_callback(self, data):
        try:
            image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
     
        try:
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            #blue
            mask_img = self.mask_f(image, self.blue_lower, self.blue_upper)
            noise_removal = self.noise_removal_f(mask_img)
            b_area = self.area_measurement_f(noise_removal)
          
            #red
            mask_image_r1 = self.mask_f(image, self.red1_lower, self.red1_upper)
            mask_image_r2 = self.mask_f(image, self.red2_lower, self.red2_upper) 
            mask_img = cv2.add(mask_image_r1, mask_image_r2)
            noise_removal = self.noise_removal_f(mask_img)
            r_area = self.area_measurement_f(noise_removal)
          
            #green
            mask_img = self.mask_f(image, self.green_lower, self.green_upper)
            noise_removal = self.noise_removal_f(mask_img)
            g_area = self.area_measurement_f(noise_removal)
            
         
            max_area = max([[b_area, 1], [r_area, 2], [g_area, 3]])
            turtle = Twist()
            if max_area[0] > 10000:
                if max_area[1] == 1:
                    turtle.linear.x = 1
                elif max_area[1] == 2:
                    turtle.linear.x = -1
                elif max_area[1] == 3:
                    turtle.angular.z = 1
                self.turtle_pub.publish(turtle)
            
        except CvBridgeError as e:
            print(e)



if __name__ == "__main__": 
    rospy.init_node("robosys2019_pub")
    robosys = Robosys()
    try:
        rospy.spin()
    except KeyboardInterrupt as e:
        print(e)
        pass

