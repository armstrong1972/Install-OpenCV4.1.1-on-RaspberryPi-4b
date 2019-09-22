# -*-coding: utf-8 -*-
# 
# 程序功能 ：使用 YOLO3 识别图片中的 object ，并返回Info
#    Info ：[left, top, width, height, classId, conf] 的集合

 
import cv2 as cv
import numpy as np

Yolo3_Classes = []

class CV_Yolo3(object):
    def __init__(self,class_path,net_width=416,net_height=416,confThreshold=0.5,nmsThreshold=0.5):
        '''
        Initialize the parameters
         :param class_path:
         :param net_width:     default 416, Width  of network's input image
         :param net_height:    default 416, Height of network's input image
         :param confThreshold: default 0.5, Confidence threshold
         :param nmsThreshold:  default 0.5, Non-maximum suppression threshold
        '''
        global Yolo3_Classes

        Yolo3_Classes = self.__read_classes(class_path)
        self.net_width=net_width
        self.net_height=net_height
        self.confThreshold=confThreshold
        self.nmsThreshold=nmsThreshold

    def __read_classes(self,file):
        with open(file, 'rt') as f:
            classes = f.read().rstrip('\n').split('\n')
        return classes
    
    def cv_dnn_init(self,modelConfiguration,modelWeights):
        self.net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
        self.net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
        #self.net.setPreferableTarget(cv.dnn.DNN_TARGET_OPENCL)      # GPU
        self.net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)        # CPU

    def __getNetLayerNames(self, net):
        # Get the names of all the layers in the network
        layersNames = net.getLayerNames()
        # Get the names of the output layers, i.e. the layers with unconnected outputs
        return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]
 
 
    def __getobjects_info(self, shape, outs):
        imgH = shape[0]
        imgW  = shape[1]
        
        classIds = []
        confidences = []
        boxes = []
        detections = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > self.confThreshold:
                    center_x = int(detection[0] * imgW)
                    center_y = int(detection[1] * imgH)
                    width  = int(detection[2] * imgW)
                    height = int(detection[3] * imgH)
                    left = int(center_x - width  / 2)
                    top  = int(center_y - height / 2)
                    classIds.append(classId)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])
 
        # NMS : 非极大值抑制(局部最大搜索)，参考文献：https://www.cnblogs.com/makefile/p/nms.html
        indices = cv.dnn.NMSBoxes(boxes, confidences, self.confThreshold, self.nmsThreshold)
        for idx in indices:
            i = idx[0]
            box    = boxes[i]
            left   = box[0]
            top    = box[1]
            width  = box[2]
            height = box[3]

            detections.append([left, top, width, height, classIds[i], confidences[i]])
        return detections
 
    def cv_dnn_forward(self,image):
        # Create a 4D blob from a image.
        blob = cv.dnn.blobFromImage(image, 1 / 255, (self.net_width, self.net_height), [0, 0, 0], 1, crop=False)
        self.net.setInput(blob)

        outs = self.net.forward(self.__getNetLayerNames(self.net))
        runtime, _ = self.net.getPerfProfile()
        return outs,runtime
 
    def yolov3_predict(self,image):
        
        outs,runtime=self.cv_dnn_forward(image)
        return self.__getobjects_info(image.shape, outs), runtime
# End of Class : cv_yolov3


# 将所有物体信息 显示出来
def Yolo3_ShowInfos(frame, dects, runtime):
    winName = 'YOLO3'
    cv.namedWindow(winName)

    for det in dects :
        left, top, width, height, classId, conf = det
        # 画方块
        cv.rectangle(frame, (left, top), (left+width, top+height), (0, 0, 255), 1)

        # 显示分类 及 %
        label = '%.2f' % conf
        # Get the label for the class name and its confidence
        if Yolo3_Classes:
            assert (classId < len(Yolo3_Classes))
            label = '%s:%s' % (Yolo3_Classes[classId], label)
        labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        top = max(top, labelSize[1])
        # 黄底 黑字
        cv.rectangle(frame, (left, top - round(1.5 * labelSize[1])), (left + round(1.5 * labelSize[0]), top + baseLine),
                        (0, 255, 255), cv.FILLED)
        cv.putText(frame, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    label = 'Inference time: %.2f ms' % (runtime * 1000.0 / cv.getTickFrequency())
    cv.putText(frame, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))

    cv.imshow(winName, frame)
    cv.waitKey(0)
    cv.destroyAllWindows()

