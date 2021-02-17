__author__ = 'will'

import pickle
import cv2
import time
import numpy as np

data = pickle.load( open( "trainingdata.p", "rb" ), encoding="latin" )
n_images = len(data)
print(n_images)
test, training = data[0:int(n_images/3)], data[int(n_images/3):]


#print (data[4200])
# print(test)

#img = data[4200][2]
#img = np.array(img,dtype=np.uint8)
#cv2.imshow('disp',np.array(cv2.resize(img,(280,280))))


cv2.namedWindow('disp')
for direcao,velocidade,img in data:
    img = np.array(img,dtype=np.uint8)
    print (direcao, velocidade)
    cv2.imshow('disp',np.array(cv2.resize(img,(280,280))))

#    time.sleep(0.05)
    cv2.waitKey(0)
cv2.destroyAllWindows()

