# Robosys_homework2
## 取得した色情報からROSのturtleを操作
   取得したカメラ映像からOpenCVを用いて色情報を取得し、その色情報に応じた動きをROSのturtleにさせる。
   turtlesimのturtlesim_nodeにTwist型のメッセージをパブリッシュすることで操作可能。
 
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

### ・参考文献
「ROSではじめるロボットプログラミング」 著者：小倉 崇　出版社：工学社

### ・実行動画
https://www.youtube.com/watch?v=sA_dwyxKMLQ&t=65s
