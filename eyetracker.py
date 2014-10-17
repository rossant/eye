import cv2
import numpy as np
import math
from math import fabs

def _is_left(target, source):
    return (fabs(target[0] - source[0,0]) < 
            fabs(target[0] - source[1,0]))

class EyeTracker(object):
    def __init__(self, image_size):
        self.image_size = image_size
        self.cascade = cv2.CascadeClassifier(
            'haarcascade_eye_tree_eyeglasses.xml')
        self.eyes = np.zeros((2, 4))

    def input(self, image):
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).T
        r = self.cascade.detectMultiScale(image.T, 1.3)
        n = len(r)
        detected_eyes = np.atleast_2d(r)
        if n >= 1:
            if _is_left(detected_eyes[0], self.eyes):
                self.eyes[0,:] = detected_eyes[0]
                if n == 2:
                    self.eyes[1,:] = detected_eyes[1]
            else:
                self.eyes[1,:] = detected_eyes[0]
                if n == 2:
                    self.eyes[0,:] = detected_eyes[1]
