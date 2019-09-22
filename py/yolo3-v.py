# coding: utf-8
# 
# 程序功能 ：调用 Yolo3 库，识别视频中的 object

import cv2 as cv
import numpy as np
import opencv_yolo3 as yolo3
import time

def openvideo(yolo, fn) :
    # 读取视频 
    cap = cv.VideoCapture(fn)     #播放指定视频文件
    #cap = cv.VideoCapture(0)     #获取摄像头视频

    if not cap.isOpened():
        print("Cannot open camera")
        exit()
        
    ok = True
    bPause = False
    while ok :
        if not bPause :
            prev_time = time.time()
            ok, img = cap.read()
            if ok :
                dects, runtime = yolo.yolov3_predict(img) # 识别图片, 返回 对象集 和 运行时间
                
                for det in dects :
                    left, top, width, height, classId, conf = det
                    # 画方块
                    cv.rectangle(img, (left, top), (left+width, top+height), (0, 0, 255), 1)

                    # 显示分类 及 %
                    label = '%.2f' % conf
                    # Get the label for the class name and its confidence
                    if yolo3.Yolo3_Classes:
                        assert (classId < len(yolo3.Yolo3_Classes))
                        label = '%s:%s' % (yolo3.Yolo3_Classes[classId], label)
                    labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                    top = max(top, labelSize[1])
                    # 黄底 黑字
                    #cv.rectangle(img, (left, top - round(1.5 * labelSize[1])),
                    #            (left + round(1.5 * labelSize[0]), top + baseLine),(0, 255, 255), cv.FILLED)       
                    cv.putText(img, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            
            cv.imshow('camera', img)
            t= time.time()-prev_time
            print("FPS = %.2f , time=%.2fs" % (1/t,t))

        k = cv.waitKey(1)
        if k == 27 :  # esc
            ok = False
        elif k==32  : # ' '
            bPause = not bPause

    cv.destroyAllWindows()
    cap.release()

if __name__ == "__main__":
    fClasses       = "./mod/dark/coco/coco.names"
    modelCfg       = "./mod/dark/coco/coco.cfg"
    modelWeights   = "./mod/dark/coco/coco.weights"

    # 初始化对象
    yolo = yolo3.CV_Yolo3(fClasses,confThreshold=0.5,nmsThreshold=0.5)
    print("Classes =" , len(yolo3.Yolo3_Classes))
    # 设置配置文件
    yolo.cv_dnn_init(modelCfg,modelWeights)

    openvideo(yolo, './img/v1.mp4')
