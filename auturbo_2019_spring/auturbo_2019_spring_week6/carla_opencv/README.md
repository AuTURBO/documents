## VNC 서버 설치

#### 사용자 비밀번호 설정
``` bash
$ sudo passwd root
```

#### ubuntu desktop 버전, 기타 패키지 설치
``` bash
$ sudo apt-get update && sudo apt-get upgrade
$ sudo apt-get install ubuntu-desktop tightvncserver gnome-panel gnome-settings-daemon metacity nautilus gnome-terminal terminator
```

#### vnc 서버를 실행하고 초기 비밀번호를 등록합니다.
``` bash
$ vncserver :1
```
#### 아래 설정파일을 수정합니다.
``` bash
$ vim ~/.vnc/xstartup
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

#### vnc 서버 재실행
``` bash
$ vncserver -kill :1
$ vncserver :1
```

#### aws 보안그룹 인바운드의 5901 포트 열어주기
- 좌측 보안그룹 메뉴 클릭
- 인바운드 탭 에서 편집 클릭 
- 규칙추가 후
 * 유형 : 사용자 지정 TCP
 * 포트범위 : 5901
 * 소스 : 내 IP

#### Remote Desktop Viewer로 원격 접속(vnc 서버 실행 후 해야함)
- connect 버튼 클릭
 * protocol : VNC 선택
 * HOST : [EC2 인스턴스 퍼블릭아이피]:1  (ex: xxx.xxx.xxx.xxx:1)
- connect 클릭




## ROS 설치
``` bash
$ sudo apt-get update && sudo apt-get upgrade &&wget https://raw.githubusercontent.com/auturbo/auturbo_robot_development_tools/master/install_ros_melodic.sh && chmod 755 ./install_ros_melodic.sh && bash ./install_ros_melodic.sh &&wget https://raw.githubusercontent.com/auturbo/auturbo_robot_development_tools/master/add_macro_for_melodic_only.sh && chmod 755 ./add_macro_for_melodic_only.sh && bash ./add_macro_for_melodic_only.sh
```
## CARLA 설치

#### python & 관련 패키지
``` bash
$ sudo apt-get install python-pip
$ pip install --user pygame numpy
```
### CARLA 다운로드 & 압축해제
```
$ wget http://carla-assets-internal.s3.amazonaws.com/Releases/Linux/CARLA_0.9.5.tar.gz
tar -zxvf CARLA_0.9.5.tar.gz
```

#### without display 모드로 Carla server 실행
 
 
``` bash
$ cd CARLA0.9.5
$ DISPLAY= ./CarlaUE4.sh
```

#### player 생성 및 컨트롤 기능 실행

``` bash
cd PythonAPI/examples
python manual_control.py
```


## CARLA ros_bridge 설치

## 내 노트북에서 rviz 띄워보기

## AWS에서 이미지 조작 하기

## autoware


>**참고자료**

>- https://steemit.com/kr/@deep-root/ubuntu-cuda (Nvidia graphic driver isntallation)
>- https://medium.com/@ggomma/%EC%9C%88%EB%8F%84%EC%9A%B0%EC%97%90%EC%84%9C-ubuntu-aws-ec2-gui-%EC%9D%B4%EC%9A%A9-ee2567a85d8f (AWS gui setting)
>- https://github.com/AuTURBO/auturbo_robot_development_tools (ROS install)
>- https://carla.readthedocs.io/en/latest/getting_started/ (Carla installation)
>- http://wiki.ros.org/dnn_detect (ROS object detection package)
>- https://github.com/carla-simulator/ros-bridge (Carla ROS bridge)
>
