# Copyright Reserved (2020).
# Donghee Lee, Univ. of Seoul
#
__author__ = 'will'

from rc_car_interface import RC_Car_Interface
from keras_learn import CNN_Driver
import numpy as np
import time
import cv2
import serial
ser = serial.Serial('/dev/serial/by-id/usb-Arduino_Srl_Arduino_Uno_754393137373514152F0-if00', 9600)

class SelfDriving:

    def __init__(self):
        self.rc_car_cntl = RC_Car_Interface()   # 인터페이스
        self.cnn_driver = CNN_Driver()          # 신경망
        self.rc_car_cntl.set_left_speed(0)
        self.rc_car_cntl.set_right_speed(0)
        self.velocity = 0                       # 속도
        self.direction = 0                      # 방향
        self.cnn_driver.keras_learn()           # 학습
    
    def rc_car_control(self, direction):
        # calculate left and right wheel speed with direction
        
        cmd = ''
        if (-0.5 < direction < 0.5):
            cmd = "F255"
        elif (0.5 <= direction):
            cmd = "R255"
        elif (direction <= -0.5):
            cmd = "L255"
        
        cmd = cmd + '\n'
        #print('My cmd is %s' % cmd)
        ser.write(cmd.encode('ascii'))

    def drive(self):
        while True:

            # For test only, (평가용 이미지 하나 가져옴)
            # img = self.dnn_driver.get_test_img()

            img = self.rc_car_cntl.get_image_from_camera()
            # img = np.reshape(img,img.shape[0]**2)

            direction = self.cnn_driver.predict_direction(img)      # float (1보다 클 수 있음)
            # print(direction)
            self.rc_car_control(direction)
            if direction != 0: time.sleep(0.1)
            else: time.sleep(0.25)
            cmd = 'F000' + '\n'
            ser.write(cmd.encode('ascii'))
            time.sleep(0.5)

if __name__ == "__main__":
    SelfDriving().drive()
