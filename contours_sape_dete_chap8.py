import cv2
import numpy as np


def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


def getContours(img):
    # To find contours of the shape
    contours, heirarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        # print(area)

        if area > 500:
            # To draw contours on the image, -1 means all contours from the image
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            # To find perimeter of the Shape
            peri = cv2.arcLength(cnt, True)
            # print(peri)

            # It will give approx shape according to peri, It returns array of points
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            # print(approx)

            # To find numbers of corners
            objCor = len(approx)
            # It will give points and width,height according to approx
            x, y, w, h = cv2.boundingRect(approx)
            # print(x,y,w,h)

            # To identify the shape based on numbers of corners
            if objCor == 3:
                objectType = "Triangle"
            elif objCor == 4:
                aspRatio = w / float(h)
                if aspRatio > 0.95 and aspRatio < 1.05:
                    objectType = "Square"
                else:
                    objectType = "Rectangle"
            elif objCor == 5:
                objectType = "Pentagon"
            elif objCor == 6:
                objectType = "Hexagon"
            elif objCor > 6:
                objectType = "Circle"
            else:
                objectType = "None"

            # To draw rectangle around the shape
            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # To put text on the image after identifying the shape
            cv2.putText(imgContour, objectType, (x + (w // 2) - 10, y + (h // 2) - 10),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 2)


path = "Resources/shapes2.png"
img = cv2.imread(path)

imgContour = img.copy()
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)

imgCanny = cv2.Canny(imgBlur, 50, 50)
getContours(imgCanny)

# cv2.imshow("Original", img)
# cv2.imshow("Image Gray", imgGray)
# cv2.imshow("Image Blur", imgBlur)

imgBlank = np.zeros_like(img)
imgStack = stackImages(0.5, ([img, imgGray, imgBlur], [imgCanny, imgContour, imgBlank]))
cv2.imshow("Image Stack", imgStack)

cv2.waitKey(0)
