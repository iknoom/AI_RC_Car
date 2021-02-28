# Copyright(c) Reserved 2020.
# Donghee Lee, University of Soul
#
__author__ = 'will'

import numpy as np
import cv2

from picameraStream import PiVideoStream

class RC_Car_Interface():

    def __init__(self):
        self.left_wheel = 0
        self.right_wheel = 0
        self.pivideo = PiVideoStream()
        self.pivideo.start()

    def set_right_speed(self, speed):
        print('set right speed to ', speed)

    def set_left_speed(self, speed):
        print('set left speed to ', speed)

    def get_image_from_camera(self):
        img = self.pivideo.read()
        img = img[:,:,0]                # 흑백으로 촬영
        threshold = int(np.mean(img)) * 0.5

        # Invert black and white with threshold
        ret, img2 = cv2.threshold(img.astype(np.uint8), threshold, 255, cv2.THRESH_BINARY_INV)
        img2 = cv2.resize(img2,(16,16), interpolation=cv2.INTER_AREA )
        # cv2.imshow("Image", img2)
        # cv2.waitKey(0)
        return img2