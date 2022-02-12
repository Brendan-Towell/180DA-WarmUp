import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):

    # Take each frame
    _, frame = cap.read()


    """
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([70,50,50])
    upper_blue = np.array([140,255,255])
    """

    # define range of blue color in BGR
    lower_blue = np.array([200, 150, 50])
    upper_blue = np.array([255, 255, 200])

    """
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    """

    # Threshold the RGB image to get only blue colors
    mask = cv2.inRange(frame, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    # Grayscale to find contours
    src_gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    src_gray = cv2.blur(src_gray, (3,3))

    threshold = 100
    canny_output = cv2.Canny(src_gray, threshold, threshold * 2)
    contours, _ = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    boxes = []
    for i in range(len(contours)):
        rect = cv2.minAreaRect(contours[i])
        boxes.append(cv2.boxPoints(rect))
        boxes[i] = np.int0(boxes[i])
    
    if(len(contours) > 0):
        largestBoxArea = cv2.contourArea(boxes[0])
        largestBox = boxes[0]
        for i in range(len(boxes)):
            if(cv2.contourArea(boxes[i]) > largestBoxArea):
                largestBox = boxes[i]
                largestBoxArea = cv2.contourArea(boxes[i])
        cv2.drawContours(frame, [largestBox], 0, (0,0,0), 3)

    cv2.imshow('frame', frame)
    cv2.imshow('res', res)
    

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()