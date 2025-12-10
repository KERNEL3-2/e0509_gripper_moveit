# E0509 + Gripper MoveIt2 Config

Doosan E0509 로봇팔 + RH-P12-RN-A 그리퍼를 위한 MoveIt2 설정 패키지

## 의존성

이 패키지를 사용하기 전에 먼저 아래 repository를 설치해야 합니다:

👉 **[e0509_gripper_description](https://github.com/fhekwn549/e0509_gripper_description)** - Gazebo 시뮬레이션 및 URDF

## 설치

### 1. 사전 패키지 설치 (위 링크의 README 참고)
```bash
# e0509_gripper_description 설치 완료 후 진행
```

### 2. 이 패키지 클론
```bash
cd ~/doosan_ws/src
git clone https://github.com/KERNEL3-2/e0509_gripper_moveit.git e0509_gripper_moveit_config
```

### 3. URDF 생성 (필수)
```bash
cd ~/doosan_ws
source install/setup.bash

# xacro → URDF 변환
xacro src/e0509_gripper_description/urdf/e0509_with_gripper.urdf.xacro use_gazebo:=false > src/e0509_gripper_moveit_config/config/e0509_gripper.urdf
```

### 4. 빌드
```bash
colcon build --symlink-install --packages-select e0509_gripper_moveit_config
source install/setup.bash
```

## 사용법

### 옵션 1: 독립 데모 (Plan 테스트용) ⚠️ Plan만 가능
```bash
ros2 launch e0509_gripper_moveit_config demo.launch.py
```

> **참고:** demo.launch.py는 실제 controller가 없어서 Plan만 가능하고 Execute는 되지 않습니다. 슬라이더로 joint 움직이며 경로 계획 테스트용입니다.

### 옵션 2: Gazebo + MoveIt2 (ros2_control) ✅ Plan & Execute 가능
```bash
# 터미널 1: Gazebo 실행
ros2 launch e0509_gripper_description gazebo.launch.py

# 터미널 2: MoveIt2 실행
ros2 launch e0509_gripper_moveit_config moveit_gazebo.launch.py
```

### 옵션 3: DART 가상로봇 + MoveIt2 ✅ Plan & Execute 가능
```bash
# 터미널 1: DART 가상로봇 실행
ros2 launch e0509_gripper_description bringup_gazebo.launch.py mode:=virtual host:=127.0.0.1 port:=12346 name:=dsr01

# 터미널 2: MoveIt2 실행
ros2 launch e0509_gripper_moveit_config moveit_dart.launch.py
```

## MoveIt2 사용

1. RViz에서 **Goal State** 드롭다운에서 `home` 선택 (또는 인터랙티브 마커 드래그)
2. **Plan** 클릭 → 경로 미리보기
3. **Execute** 클릭 → Gazebo/DART 로봇 실행 (옵션 2, 3만 가능)

## URDF 재생성 (원본 xacro 수정 시)

`e0509_gripper_description`의 xacro 파일을 수정한 경우, 위 설치 3단계를 다시 실행하세요.

## 파일 구조
```
e0509_gripper_moveit_config/
├── config/
│   ├── e0509_gripper.urdf      # 로봇 URDF (xacro에서 생성)
│   ├── dsr.srdf                # MoveIt semantic description
│   ├── kinematics.yaml         # IK solver 설정
│   └── moveit_controllers.yaml # Controller 설정
├── launch/
│   ├── demo.launch.py          # 독립 데모 (Plan만)
│   ├── moveit_gazebo.launch.py # Gazebo 연동 (Plan & Execute)
│   └── moveit_dart.launch.py   # DART 가상로봇 연동 (Plan & Execute)
└── README.md
```

## 관련 링크

- [e0509_gripper_description](https://github.com/fhekwn549/e0509_gripper_description) - Gazebo 시뮬레이션
- [doosan-robot2](https://github.com/doosan-robotics/doosan-robot2) - 두산 공식 ROS2 드라이버
- [RH-P12-RN-A](https://github.com/ROBOTIS-GIT/RH-P12-RN-A) - 그리퍼 패키지
