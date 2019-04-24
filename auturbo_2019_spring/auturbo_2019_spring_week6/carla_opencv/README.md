## 1. AWS EC2 인스턴스 생성 및 접속
#### 1.1. 인스턴스 유형 p2.xlarge 선택

#### 1.2. EBS 볼륨
크기 : 30GiB
삭제 : 체크 해제
EBS 최적화 인스턴스 : 체크

#### 1.3. 보안그룹
|유형|프로토콜|포트범위|소스|
|---|---|---|---|
|SSH|TCP|22|내 IP|
|사용자 지정 TCP 규칙|TCP|5901|내 IP|
|사용자 지정 TCP 규칙|TCP|11311|내 IP|

#### 1.4. 키 페어
키가 없는경우 새로 생성하기를 선택하면되며 다운로드 한 키는 잘 보관해야합니다.
키를 github등 공유 가능한 곳에 올리지 않도록 주의해야합니다.

#### 1.5. EC2 인스턴스에 ssh로 접속하기
ssh -i [키 경로] ubuntu@[IPv4 퍼블릭 IP]


## 2. VNC 서버 설치

#### 2.1. 사용자 비밀번호 설정
``` bash
$ sudo passwd root
```

#### 2.2. ubuntu desktop 버전, Nvidia graphic drive, 기타 패키지 설치
``` bash
$ sudo apt-get update && sudo apt-get upgrade
$ sudo apt-get install ubuntu-desktop tightvncserver gnome-panel gnome-settings-daemon metacity nautilus gnome-terminal terminator
$ sudo add-apt-repository ppa:graphics-drivers/ppa
$ sudo apt-get update
$ sudo ubuntu-drivers autoinstall
$ sudo reboot
```

#### 2.3. vnc 서버를 실행하고 초기 비밀번호를 등록합니다.
``` bash
$ vncserver :1
```
#### 2.4. 아래 설정파일을 수정합니다.
``` bash
$ sudo vim ~/.vnc/xstartup
```

```
#!/bin/sh

export XKL_XMODMAP_DISABLE=1
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS

[ -x /etc/vnc/xstartup ] && exec /etc/vnc/xstartup
[ -r $HOME/.Xresources ] && xrdb $HOME/.Xresources
xsetroot -solid grey

vncconfig -iconic &
gnome-panel &
gnome-settings-daemon &
metacity &
nautilus &
gnome-terminal &

```

#### 2.5. vnc 서버 재실행
``` bash
$ vncserver -kill :1
$ vncserver :1
```

#### 2.6. aws 보안그룹 인바운드의 5901 포트 열어주기
- 좌측 보안그룹 메뉴 클릭
- 인바운드 탭 에서 편집 클릭 
- 규칙추가 후
 * 유형 : 사용자 지정 TCP
 * 포트범위 : 5901
 * 소스 : 내 IP

#### 2.7. Remote Desktop Viewer로 원격 접속(vnc 서버 실행 후 해야함)
- connect 버튼 클릭
 * protocol : VNC 선택
 * HOST : [EC2 인스턴스 퍼블릭아이피]:1  (ex: xxx.xxx.xxx.xxx:1)
- connect 클릭




## 3. ROS 설치
``` bash
$ sudo apt-get update && sudo apt-get upgrade &&wget https://raw.githubusercontent.com/auturbo/auturbo_robot_development_tools/master/install_ros_melodic.sh && chmod 755 ./install_ros_melodic.sh && bash ./install_ros_melodic.sh &&wget https://raw.githubusercontent.com/auturbo/auturbo_robot_development_tools/master/add_macro_for_melodic_only.sh && chmod 755 ./add_macro_for_melodic_only.sh && bash ./add_macro_for_melodic_only.sh
```
## 4. CARLA 설치

#### 4.1 python & 관련 패키지
``` bash
$ sudo apt-get install python-pip
$ pip install --user pygame numpy
```
#### 4.2 CARLA 다운로드 & 압축해제
```
$ mkdir ~/Downloads/CARLA
$ cd ~/Downloads/CARLA
$ wget http://carla-assets-internal.s3.amazonaws.com/Releases/Linux/CARLA_0.9.5.tar.gz
tar -zxvf CARLA_0.9.5.tar.gz
```

#### 4.3 without display 모드로 Carla server 실행
 
 
``` bash
$ cd CARLA0.9.5
$ DISPLAY= ./CarlaUE4.sh
```

#### 4.4 player 생성 및 컨트롤 기능 실행

``` bash
$ cd PythonAPI/examples
$ python manual_control.py
```


## 5. CARLA ros_bridge 설치
```bash
$ git clone https://github.com/carla-simulator/ros-bridge.git
$ cd ..
$ rosdep update
$ rosdep install --from-paths src --ignore-src -r
$ catkin_make
```

```bash
$ eb
맨 아랫줄에 추가
export PYTHONPATH=$PYTHONPATH:~/Downloads/CARLA/PythonAPI/carla/dist/carla-0.9.5-py2.7-linux-x86_64.egg
```

## 6. 내 노트북에서 rviz 띄워보기

#### 6.1. ip 설정
|---|aws|내PC|
|ROS_MASTER_URI|aws 프라이빗 ip|aws 퍼블릭 ip|
|ROS_HOSTNAME|aws 퍼블릭 ip|내 PC ip|

#### 6.2. 내 PC와 aws 인스턴스 둘 다 에서 실행
```bash
$ cd ~/Downloads
$ git clone https://github.com/AuTURBO/documents
$ cp -r ~/Downloads/documents/auturbo_2019_spring/auturbo_2019_spring_week6/carla_opencv ~/catkin_ws/src/
```


#### 6.3. aws 인스턴스에서 실행
```bash
$ rosrun carla_opencv 1publisher.py
```


#### 6.1. 내 PC에서 실행
```bash
$ rosrun carla_opencv 2display_image.py
```


## 7. AWS에서 이미지 조작 하기

#### 7.1. Hough transform (AWS에서)
``` bash
$ rosrun carla_opencv 3houghLine.py
```


>**참고자료**

>- https://steemit.com/kr/@deep-root/ubuntu-cuda (Nvidia graphic driver isntallation)
>- https://medium.com/@ggomma/%EC%9C%88%EB%8F%84%EC%9A%B0%EC%97%90%EC%84%9C-ubuntu-aws-ec2-gui-%EC%9D%B4%EC%9A%A9-ee2567a85d8f (AWS gui setting)
>- https://github.com/AuTURBO/auturbo_robot_development_tools (ROS install)
>- https://carla.readthedocs.io/en/latest/getting_started/ (Carla installation)
>- http://wiki.ros.org/dnn_detect (ROS object detection package)
>- https://github.com/carla-simulator/ros-bridge (Carla ROS bridge)
>
