__author__ = 'will'

import pickle
import cv2
import numpy as np

data = pickle.load(open("train_img_final516.p", "rb"), encoding="latin")
n_images = len(data)
print("n_images :", n_images)

cv2.namedWindow('disp')
for i in range(n_images):
    d, v, img = data[i]
    img = np.array(img, dtype=np.uint8)
    cv2.imshow('disp', np.array(cv2.resize(img, (280, 280))))
    print(i, ":", d, v)
    cv2.waitKey(0)

cv2.destroyAllWindows()