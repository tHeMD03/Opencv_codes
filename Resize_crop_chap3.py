import cv2
import numpy as np

img = cv2.imread("Resources/1.png")
# To find size of img, o/p:(Height, Width, no of channels BGR)
print(img.shape)

# To resize the img (width, Height)
img_resize = cv2.resize(img, (450, 542))
print(img_resize.shape)

# To crop img (height, width)
img_crop = img[200:400, 0:800]
print(img_crop.shape)

cv2.imshow("Output", img)
cv2.imshow("Resized Output", img_resize)
cv2.imshow("Cropped Output", img_crop)
cv2.waitKey(0)
