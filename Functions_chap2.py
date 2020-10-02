import cv2
import numpy as np

img = cv2.imread("Resources/1.png")

# Numpy to create matrix of size 5x5 , uint8 = unsigned int 8bits (0-255)
kernel = np.ones((5,5), np.uint8) # ones means all 1s

# cv2.cvtcolor - to convert the image into grayscale or any other
# RGB = BGR in Opencv
imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# To add gaussian Blur ksize should be odd nums
imgblur = cv2.GaussianBlur(imggray, (11, 11), 0)

# To detect edges in the image
imgCanny = cv2.Canny(img, 100, 100)

# When we can't get edges properly (thik edges)
imgdialate = cv2.dilate(imgCanny, kernel, iterations=1)

# Thin edges - opp. of dialation
imgerode = cv2.erode(imgdialate, kernel, iterations=2)

cv2.imshow("Gray output", imggray)
cv2.imshow("Blured output", imgblur)
cv2.imshow("Canny output", imgCanny)
cv2.imshow("Dialation output", imgdialate)
cv2.imshow("Eroded output", imgerode)
cv2.waitKey(0)
