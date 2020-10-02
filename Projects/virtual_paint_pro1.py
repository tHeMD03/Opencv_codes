import cv2
import numpy as np

frame_w = 640
frame_h = 480
cap = cv2.VideoCapture(0)
cap.set(3, frame_w)
cap.set(4, frame_h)
cap.set(10, 150)

# [48, 114, 129, 116, 255, 208], blue, 12 136 106 21 255 255
myColors = [[12, 136, 106, 21, 255, 255],
            [57, 53, 44, 84, 255, 255], [107, 43, 60, 131, 162, 255]]

# color values in BGR
mycolorvalue = [[3, 190, 252],
                [0, 184, 9],
                [176, 26, 134]]

mypoints = []  # [x, y, colorID]


def findColor(img, myColors, mycolorvalue):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0  # it is for diff color for diff markers
    newpoints = []  # to get the points x,y according to contours
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)
        # cv2.circle(imgresult, (x, y), 10, mycolorvalue[count], cv2.FILLED)
        if x != 0 and y != 0:
            newpoints.append([x, y, count])
        count += 1
        # cv2.imshow(str(color[0]),mask)
    return newpoints


def getContours(img):
    contours, heirarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0  # If contours is not found then all points will be 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            # cv2.drawContours(imgresult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    # We want to drw from tip or center
    return x + w // 2, y


def drawOnCanvas(mypoints, mycolorvalue):
    for point in mypoints:
        cv2.circle(imgresult, (point[0], point[1]), 10, mycolorvalue[point[2]],
                   cv2.FILLED)  # draw circles according to values of mypoints


while True:
    success, img = cap.read()
    imgresult = img.copy()
    newpoints = findColor(img, myColors, mycolorvalue)
    if len(newpoints) != 0:
        for newp in newpoints:
            mypoints.append(newp)  # adding points int the mypoints
    if len(mypoints) != 0:
        drawOnCanvas(mypoints, mycolorvalue)
    cv2.imshow("Result", imgresult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
