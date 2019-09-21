# Install-OpenCV4.1.1-on-RaspberryPi-4b
How to install OpenCV4.1.1 on RaspberryPi 4b

Provide Chinese version first, English later


安装系统
==========

1: 下载 SD Card Formatter （https://www.sdcard.org/downloads/formatter/index.html）
    用 SD Card Formatter 格式化 cf 卡
    
2：下载NOOBS_v3_2_0.zip （https://www.raspberrypi.org/downloads/noobs/）
    unzip所有文件到cf卡根目录

3：cf卡插入树莓派，开机启动。


打开 摄像头、SSH、VNC 等
==========================
主菜单->Preferences->Raspberry Pi Configuration
在Interface选项卡中进行选择



换源 (如果安装时选了 地区：中国，语言：中文，自动为清华源)
==============================================================
$ sudo nano /etc/apt/sources.list
注释掉原数据行，增加如下2行
科大源：
deb http://mirrors.ustc.edu.cn/raspbian/raspbian/ stretch main contrib non-free rpi
deb-src http://mirrors.ustc.edu.cn/raspbian/raspbian/ stretch main contrib non-free rpi
清华源：
deb https://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ stretch main contrib non-free rpi
deb-src https://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ stretch main contrib non-free rpi
阿里云：
deb http://mirrors.aliyun.com/raspbian/raspbian/ stretch main contrib non-free rpi
deb-src http://mirrors.aliyun.com/raspbian/raspbian/ stretch main contrib non-free rpi

$ sudo apt-get update             #更新软件版本目录清单
$ sudo apt-get upgrade            #更新软件


安装 摄像头
==============
USB先不插入摄像头
$ lsusb
插入摄像头后再运行一遍，如果有多出的设备，表示已被系统接受。如，多出：
Bus 001 Device 004: ID 0bda:58b0 Realtek Semiconductor Corp. 

拍照测试
$ sudo apt-get install fswebcam
$ fswebcam /dev/video0 image.jpg
查看Home目录下的 image.jpg 是否正常

设置为网络摄像头
$ sudo apt-get install motion
$ sudo nano /etc/default/motion
将 start_motion_daemon 由no改为yes，后台执行

$ sudo nano /etc/motion/motion.conf
^w快速查找 并 修改如下参数 : 
daemon on
stream_localhost off
webcontrol_localhost off
width 500 
height 400

启动motion
$ sudo motion
在其它计算机打开 http://树莓派IP:8080

退出motion
$ service motion stop



在树莓派设置中把根目录扩大到整个SD卡 (Pi4B已不需要)
====================================================
安装OpenCV、Dlib、Darknet等需要很大空间，不扩大会安装失败
$ sudo raspi-config
选7 Adv Options，再选A1。退出后重启
$ sudo reboot



安装 基础库
===============
$ sudo apt-get install build-essential cmake unzip pkg-config
$ sudo apt-get -y install libjpeg-dev libpng-dev libtiff-dev
$ sudo apt-get -y install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
$ sudo apt-get -y install libxvidcore-dev libx264-dev
$ sudo apt-get -y install libgtk-3-dev
$ sudo apt-get -y install libcanberra-gtk*
$ sudo apt-get -y install libatlas-base-dev gfortran
$ sudo apt-get -y install python3-dev


安装 OpenCV
==============
从 https://github.com/opencv 下载：
    opencv-4.1.1.zip
    opencv_contrib-4.1.1.zip
    
$ unzip opencv-4.1.1.zip
$ unzip opencv_contrib-4.1.1.zip
$ cd opencv-4.1.1
目录改名，方便抄前人文档的cmake参数
$ mv opencv-4.1.1 opencv
$ mv opencv_contrib-4.1.1 opencv_contrib

升级pip
$ wget https://bootstrap.pypa.io/get-pip.py
$ sudo python3 get-pip.py

$ sudo pip3 install numpy

创建build目录，并编译
$ cd opencv
$ mkdir build
$ cd build
请自行修改 OPENCV_EXTRA_MODULES_PATH 的值（本人2个zip下载到 ~/ai/opencv下）
可以用ls一下目录，确认由文件显示后，作为参数值
$ cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=~/ai/opencv/opencv_contrib/modules \
    -D ENABLE_NEON=ON \
    -D ENABLE_VFPV3=ON \
    -D BUILD_TESTS=OFF \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D CMAKE_SHARED_LINKER_FLAGS='-latomic' \
    -D BUILD_EXAMPLES=OFF ..

$ make -j4
查找如下输出内容，表示成功
[100%] Built target opencv_python2
[100%] Linking CXX shared module ../../lib/python3/cv2.cpython-37m-arm-linux-gnueabihf.so
[100%] Built target opencv_python3

$ sudo make install
查找如下输出内容，表示成功
-- Installing: /usr/local/lib/python3.7/dist-packages/cv2/python-3.7/cv2.cpython-37m-arm-linux-gnueabihf.so
-- Set runtime path of "/usr/local/lib/python3.7/dist-packages/cv2/python-3.7/cv2.cpython-37m-arm-linux-gnueabihf.so" to "/usr/local/lib"

$ sudo ldconfig

检测是否成功：
$ python3
>>> import cv2
>>> cv2.__version__
'4.1.1'

OK,结束。
