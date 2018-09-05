from styx_msgs.msg import TrafficLight
import cv2
import numpy as np



class TLClassifier(object):

    def __init__(self):

        ## initial the red mask range
        self.min_red1 = np.array([0, 100, 70])
        self.max_red1 = np.array([10, 256, 256])

        self.min_red2 = np.array([170, 100, 70])
        self.max_red2 = np.array([180, 256, 256])

    def get_classification(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_blur = cv2.GaussianBlur(image, (7,7), 0)
        image_blur_hsv = cv2.cvtColor(image_blur, cv2.COLOR_RGB2HSV)

        ## apply the red mask
        mask1 = cv2.inRange(image_blur_hsv, self.min_red1, self.max_red1)
        mask2 = cv2.inRange(image_blur_hsv, self.min_red2, self.max_red2)
        mask = mask1 + mask2

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))
        mask_closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask_clean = cv2.morphologyEx(mask_closed, cv2.MORPH_OPEN, kernel)
        _, contours, _ = cv2.findContours(mask_clean, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            return TrafficLight.RED
        else:
            return TrafficLight.UNKNOWN

