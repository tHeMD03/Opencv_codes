import cv2

# Image loading

# img = cv2.imread("Resources/1.png")
# cv2.imshow("Output", img)
# cv2.waitKey(0)  # to add delay(ms)

# Video loading

# cap = cv2.VideoCapture("Resources/video.mp4")
#
# while True:
#     success, img = cap.read()
#     cv2.imshow("Video Output",img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break


# Using webcam

cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Width(ID=3) of the window
cap.set(4, 480)  # Height(ID=4) of the window
cap.set(10, 150)  # Brightness(ID=10)

while True:
    success, img = cap.read()
    cv2.imshow("Video Output", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
