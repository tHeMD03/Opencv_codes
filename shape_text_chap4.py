import cv2
import numpy as np

# To generate pixels using numpy ((height,width,channels))
img = np.zeros((512, 512, 3), np.uint8)
print(img.shape)

# : is used for the range in which we want the color
# img[:] = 0, 0, 255

# range as per the cropping (height,width)
# img[200:300,100:300] = 0, 255, 0

# (img name, starting point, end point, color, thickness)
# cv2.line(img, (0, 0), (300, 300), (0, 0, 255), 3)

# OR img.shape we can get height and width directly to get full diagonal line
cv2.line(img, (0, 0), (img.shape[1], img.shape[0]), (0, 0, 255), 3)

# To draw rectangle (same as line) to fill rectangle cv2.FILLED in place of thickness
cv2.rectangle(img, (0, 0), (250, 350), (0, 255, 0), 2)

# to Draw circle (img name,cener point,radius,color,thickness)
cv2.circle(img, (400, 50), 30, (255, 255, 0), 5)

# To show twxt on image (img name,text, startpoint , font , scale, color, thickness)
cv2.putText(img, "Opencv Text", (250, 250), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 1)

cv2.imshow("Shape and Text", img)
cv2.waitKey(0)
