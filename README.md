# Robosys_homework2
## 取得した色情報からROSのturtleを操作
   取得したカメラ映像からOpenCVを用いて色情報を取得し、その色情報に応じた動きをROSのturtleにさせる。
   turtlesimのturtlesim_nodeにgeometry_msgs/Twist型のメッセージをパブリッシュすることで操作可能。
  　青色を認識した場合は「前進」
   
    赤色を認識した場合は「後退」
    
    緑色を認識した場合は「左旋回」
 
### ・実行環境
OS ... Ubuntu 18.04 LTS

ROS_version ... melodic

使用言語　... Python

カメラ ... UVC規格に対応したもの

### ・インストールが必要なパッケージ
~~~~
$ sudo apt install ros-melodic-usb-cam
~~~~

### ・実行方法
~~~~
$ roslaunch robosys robosys.launch
~~~~

### ・参考書
「ROSではじめるロボットプログラミング」 著者：小倉 崇　出版社：工学社

### ・実行動画
https://www.youtube.com/watch?v=sA_dwyxKMLQ&t=65s
