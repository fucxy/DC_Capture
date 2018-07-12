import cv2
import numpy as np
import sys
from time import sleep
from tkinter import *
from tkinter.ttk import *
import threading
close_prog = 0
win=Tk()
win.title("DCDetect")


















def core():
  if len(sys.argv) != 2:
      print("Usage: python3 XXX.py XXX.mov")
      sys.exit(0)

  # Open File
  if sys.argv[1] == "1":
    cap = cv2.VideoCapture(1)
  else:
    cap = cv2.VideoCapture(sys.argv[1])
  gap = 5
  max_c_def = 2000
  # Setting Windows size
  width = 640
  height = 480
  area = width * height
  #cv2.resize(cap, (400, 400), interpolation=cv2.INTER_LINEAR)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

  ret , frame = cap.read()
  avg = cv2.blur(frame, (4, 4))
  avg_float = np.float32(avg)

  history_box = []
  history_car = []
  history_mask = []

  while(cap.isOpened()):
    # 讀取一幅影格
    ret, frame = cap.read()
    orig_frame = frame
    # 若讀取至影片結尾，則跳出
    if ret == False:
      break

    # 模糊處理
    blur = cv2.blur(frame, (4, 4))

    # 計算目前影格與平均影像的差異值
    diff = cv2.absdiff(avg, blur)

    # 將圖片轉為灰階
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # 篩選出變動程度大於門檻值的區域
    ret, thresh = cv2.threshold(gray, 15, 255, cv2.THRESH_BINARY)

    # 使用型態轉換函數去除雜訊
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    # 產生等高線
    cntImg, cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    has_car = 0
    two_car = 0
    max_c = max_c_def
    max_c_2 = max_c_def
    cur_box = []
    for c in cnts:
      # 忽略太小的區域
      if cv2.contourArea(c) < max_c_def:
        continue
      if max_c < cv2.contourArea(c):
        if max_c != max_c_def:
          two_car = 1
          max_c_2 = max_c
          max_obj_2 = max_obj 
        max_c = cv2.contourArea(c)
        max_obj = c
        has_car = 1
        # 偵測到物體，可以自己加上處理的程式碼在這裡...
        rect = cv2.minAreaRect(c)
        print (rect)
        cur_box = cv2.cv2.boxPoints(rect)
        cur_box = np.int0(cur_box)
        print(cur_box)
        

      
    # 畫出等高線（除錯用）
    i = 0
    for box in history_box:
      if i % gap == 0:
        cv2.drawContours(frame, [box], 0, (255, 255, 255), 2)
      i = i + 1
    i = 0
    for obj in history_car:
      if i % gap == 0:
        frame = cv2.bitwise_and(frame, frame, mask=history_mask[i])
        frame = cv2.bitwise_xor(frame, obj)
        #cv2.drawContours(frame, [obj], 0, (255, 255, 255), 2)

      i = i + 1
    if has_car == 1:
      mask = np.zeros(frame.shape[:2],np.uint8)
      cv2.drawContours(mask, [max_obj],-1, 255, -1)
      if two_car == 1:
        cv2.drawContours(mask, [max_obj_2],-1, 255, -1)
      max_obj = cv2.bitwise_and(orig_frame, orig_frame, mask=mask)
      #cv2.drawContours(frame, max_obj, -1, (0, 255, 255), 2)
      #cv2.drawContours(frame, [cur_box], 0, (255, 255, 255), 2)
      history_box.append(cur_box)
      history_car.append(max_obj)
      mask = cv2.bitwise_not(mask)
      history_mask.append(mask)
    
    #frame = cv2.resize(frame,(0,0),fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
    # 顯示偵測結果影像
    if has_car == 1:
      cv2.imshow('frame', frame)
    else:
      history_box = []
      history_car = []
      history_mask = []

    if cv2.waitKey(1) & 0xFF == ord('q') and close_prog == 1:
      close_prog = 0
      break

    # 更新平均影像
    cv2.accumulateWeighted(blur, avg_float, 0.01)
    avg = cv2.convertScaleAbs(avg_float)

  cap.release()
  cv2.destroyAllWindows()



def clickStart():
  t1 = threading.Thread(target=core)
  t1.start()
  t1.join()
  statuslabel.config(text="Start prog")
def clickStop():
  statuslabel.config(text="Stop")
  close_prog = 1
  statuslabel.config(text="Start prog")
def clickExit():
  sys.exit(0)



statuslabel=Label(win, text="Hello World!")
carsize_label=Label(win, text="Car Size(Def:3000):")
carsize_entry=Entry(win)
carsize_entry.insert(END,'3000')
startbutton=Button(win, text="Start", command=clickStart)
stopbutton=Button(win, text="Stop", command=clickStop)
exitbutton=Button(win, text="Exit", command=clickExit)
statuslabel.grid(row = 0,column=1)
carsize_label.grid(row = 1 ,column=0)
carsize_entry.grid(row = 1 ,column=1)
startbutton.grid(row =2,column=0)
stopbutton.grid(row =2,column=1)
exitbutton.grid(row=2,column=2)
win.mainloop()