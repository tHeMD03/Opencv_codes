import cv2
import numpy as np

img = cv2.imread("Resources/cards.jpg")

width, height = 250, 350

# Array of Points of the original image
pts1 = np.float32([[303, 72], [454, 68], [312, 258], [481, 249]])

# Array of Points of the o/p image to shown
pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

# matrix for the image
matrix = cv2.getPerspectiveTransform(pts1, pts2)

# Warp perspective og image
img_out = cv2.warpPerspective(img, matrix, (width, height))


cv2.imshow("cards", img)
cv2.imshow("Warp", img_out)
cv2.waitKey(0)
