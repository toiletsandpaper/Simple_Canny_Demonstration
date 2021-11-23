import cv2
print(cv2.__file__)

def canny_webcam():
    "Live capture frames from webcam and show the canny edge image of the captured frames."

    aperture_size = 3
    edges_size = 50

    cap = cv2.VideoCapture('crowd1.mp4')

    while cap.isOpened():
        ret, frame = cap.read()  # ret gets a boolean value. True if reading is successful (I think). frame is an
        # uint8 numpy.ndarray

        frame = cv2.GaussianBlur(frame, (7, 7), 1.41)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        edge = cv2.Canny(frame, 25, 75, apertureSize=aperture_size)

        cv2.imshow('Canny Edge', edge)

        if cv2.waitKey(20) == ord('q'):  # Introduce 20 milisecond delay. press q to exit.
            break

canny_webcam()