import cv2
import numpy as np

def empty(a):
    pass

cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars", 640, 240)

# Hue trackbar (Track name, trackbar name, min hue, max hue(179 in opencv), changing function)
cv2.createTrackbar("Hue Min", "Trackbars", 9, 179, empty)
cv2.createTrackbar("Hue Max", "Trackbars", 27, 179, empty)
cv2.createTrackbar("Sat Min", "Trackbars", 74, 255, empty)
cv2.createTrackbar("Sat Max", "Trackbars", 255, 255, empty)
cv2.createTrackbar("Value Min", "Trackbars", 0, 255, empty)
cv2.createTrackbar("Value Max", "Trackbars", 255, 255, empty)


cap = cv2.VideoCapture(0)
cap.set(3, 300)  # Width(ID=3) of the window
cap.set(4, 300)  # Height(ID=4) of the window
cap.set(10, 120)  # Brightness(ID=10)

while True:
    success, img = cap.read()
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("Hue Min", "Trackbars")
    h_max = cv2.getTrackbarPos("Hue Max", "Trackbars")
    s_min = cv2.getTrackbarPos("Sat Min", "Trackbars")
    s_max = cv2.getTrackbarPos("Sat Max", "Trackbars")
    v_min = cv2.getTrackbarPos("Value Min", "Trackbars")
    v_max = cv2.getTrackbarPos("Value Max", "Trackbars")
    print(h_min,s_min,v_min,h_max,s_max,v_max)

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHSV, lower, upper)

    imgResult = cv2.bitwise_and(img, img, mask=mask)

    cv2.imshow("Video Output", img)
    cv2.imshow("Mask", mask)
    cv2.imshow("ImgResult", imgResult)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break