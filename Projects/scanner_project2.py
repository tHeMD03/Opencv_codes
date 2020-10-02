import cv2
import numpy as np

widthimg = 640
heightimg = 480

cap = cv2.VideoCapture(0)
cap.set(3, widthimg)  # Width(ID=3) of the window
cap.set(4, heightimg)  # Height(ID=4) of the window
cap.set(10, 150)  # Brightness(ID=10)


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


def preprocessing(img):
    imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgblur = cv2.GaussianBlur(imggray, (5, 5), 1)
    imgcanny = cv2.Canny(imgblur, 200, 200)
    kernel = np.ones((5, 5))
    imgdial = cv2.dilate(imgcanny, kernel, iterations=2)
    imgthre = cv2.erode(imgdial, kernel, iterations=1)

    return imgthre


def getContours(img):
    # To find contours of the shape
    contours, heirarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    biggest = np.array([])
    maxarea = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)

        if area > 500:
            # To draw contours on the image, -1 means all contours from the image
            # cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            # To find perimeter of the Shape
            peri = cv2.arcLength(cnt, True)
            # It will give approx shape according to peri, It returns array of points
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            if area > maxarea and len(approx) == 4:
                biggest = approx
                maxarea = area

            # print(len(approx))
    cv2.drawContours(imgContour, biggest, -1, (255, 0, 0), 15)
    return biggest

    # # To find numbers of corners
    # objCor = len(approx)
    # # It will give points and width,height according to approx
    # x, y, w, h = cv2.boundingRect(approx)


def reorder(mypoints):
    # if len(mypoints) == 4:
    mypoints = mypoints.reshape((4, 2))
    mypointsnew = np.zeros((4, 1, 2), np.int32)
    add = mypoints.sum(axis=1)

    mypointsnew[0] = mypoints[np.argmin(add)]
    mypointsnew[3] = mypoints[np.argmax(add)]

    diff = np.diff(mypoints, axis=1)
    mypointsnew[1] = mypoints[np.argmin(diff)]
    mypointsnew[2] = mypoints[np.argmax(diff)]

    return mypointsnew
    # else:
    #     mypoints = np.float32([[0, 0], [widthimg, 0], [0, heightimg], [widthimg, heightimg]])
    #     return mypoints


def getwarp(img, biggest):
    biggest = reorder(biggest)
    # Array of Points of the original image
    # if len(biggest) == 4:
    pts1 = np.float32(biggest)
    # else:
    #     pts1 = np.float32([[0, 0], [widthimg, 0], [0, heightimg], [widthimg, heightimg]])
    # [[303, 72], [454, 68], [312, 258], [481, 249]]
    # Array of Points of the o/p image to shown
    pts2 = np.float32([[0, 0], [widthimg, 0], [0, heightimg], [widthimg, heightimg]])

    # matrix for the image
    matrix = cv2.getPerspectiveTransform(pts1, pts2)

    # Warp perspective og image
    img_out = cv2.warpPerspective(img, matrix, (widthimg, heightimg))

    return img_out


while True:
    success, img = cap.read()
    cv2.resize(img, (widthimg, heightimg))
    imgContour = img.copy()
    imgthre = preprocessing(img)
    biggest = getContours(imgthre)
    # print(biggest)
    if biggest.size >= 4:
        warpview = getwarp(img, biggest)

        imgarray = [[img, imgthre],
                    [imgContour, warpview]]
        cv2.imshow("Final Scan", warpview)
    else:
        imgarray = [[img, imgthre],
                    [img, img]]

    stackimages = stackImages(0.6, imgarray)

    cv2.imshow("WorkFlow", stackimages)
    # cv2.imshow("Final Scan", warpview)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
