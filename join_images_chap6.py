import cv2
import numpy as np

img = cv2.imread("Resources/ml.jpg")

# hstack to show images horizontally
imgHor = np.hstack((img, img, img))

# vstack to show images vertical
imgVer = np.vstack((img, img))

cv2.imshow("Horizontal", imgHor)
cv2.imshow("Vertical", imgVer)
cv2.waitKey(0)
