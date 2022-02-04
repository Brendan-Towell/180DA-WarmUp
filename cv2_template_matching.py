import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

template = cv.imread('mask_template.jpg')
w, h = template.shape[1], template.shape[0]

while(1):

    # Take each frame
    _, frame = cap.read()
    cv.imshow('frame',frame)
    
    
    # Apply template matching to the frame
    res = cv.matchTemplate(frame, template, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv.rectangle(frame,top_left, bottom_right, 255, 2)

    cv.imshow('later frame', frame)
    

    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

cv.destroyAllWindows()