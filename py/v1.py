# coding: utf-8
# 
# 程序功能 ：抓取摄像头，[并转为灰度视频]

import numpy as np
import cv2 as cv

#video = 'http://admin:admin@192.168.1.254/jpg_stream'  # 测试成功
#cap = cv.VideoCapture(video)  #网络摄像头
cap = cv.VideoCapture(0)       #本地摄像头
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv.imshow('frame', frame)
    if cv.waitKey(1) == 27: # Esc
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()