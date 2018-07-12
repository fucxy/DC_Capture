import numpy as np
import cv2 
cap = cv2.VideoCapture('IMG_0269.MOV') 
fgbg = cv2.bgsegm.BackgroundSubtractorMOG()
while(1):
  ret, frame = cap.read()
  fgmask = fgbg.apply(frame) 
  fgmask = cv2.resize(fgmask,(0,0),fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
  cv2.imshow('frame',fgmask)
  k = cv2.waitKey(30) & 0xff
  if k == 27:
    break 
cap.release()
cv2.destroyAllWindows()