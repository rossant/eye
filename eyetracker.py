import cv2
import numpy as np
import math
from math import fabs

class EyeTracker(object):
    def __init__(self, image_size):
        self.image_size = image_size
        self.cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
        self.eyes = np.zeros((2, 4))

    def input(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).T
        detected_eyes = self.cascade.detectMultiScale(gray, 1.3)
        if len(detected_eyes) == 1:
            if (fabs(detected_eyes[0][0] - self.eyes[0,0]) < 
                fabs(detected_eyes[0][1] - self.eyes[1,0])):
                self.eyes[0,:] = detected_eyes
            else:
                self.eyes[1,:] = detected_eyes
        elif len(detected_eyes) == 2:
            self.eyes[:] = detected_eyes
