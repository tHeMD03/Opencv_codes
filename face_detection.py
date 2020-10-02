import cv2

'''This is Face detection using Viola & Jones method
Dataset that is used here is haarcascade_frontalface_default '''

facecascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Width(ID=3) of the window
cap.set(4, 480)  # Height(ID=4) of the window
cap.set(10, 150)  # Brightness(ID=10)

while True:
    success, img = cap.read()

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # To detect the faces
    faces = facecascade.detectMultiScale(imgGray, 1.1, 4)
    # print(faces)

    for (x, y, w, h) in faces:
        cv2.putText(img, "Face", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow("Output", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
