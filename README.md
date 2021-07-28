# segbot-ur5
The repo builds on BWI project of UTAustin and contains a mobile manipulator platform in gazebo.

## Requirments
Make sure you have installed ROS Melodic and ROS_DISTRO environment variable is set correctly.

## Installation

Create workspace and download repo:
```
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws
wstool init src https://raw.githubusercontent.com/keke-220/segbot-ur5/master/rosinstall/melodic.rosinstall
```

Install dependencies:
```
rosdep update
rosdep install --from-paths src --ignore-src --rosdistro $ROS_DISTRO -y
```

Build everything and source workspace:
```
catkin build -j6
source devel/setup.bash
```

## Usage
Launch banquet environment and bring up mobile manipulator:
```
roslaunch tamp_perception segbot_ur5.launch
```

Open another terminal and test with a simple pick&place task:
```
source ~/catkin_ws/devel/setup.bash
rosrun tamp_perception pick_n_place.py
```
# Task-Motion-Plan-with-GPT3
this repo builds on BingU SUNY AIR lab's mobile manipulator platform in gazebo. [segbot-ur5](https://github.com/keke-220/segbot-ur5)
## Requirments
Make sure the segbot-ur5 is installed and set correctly
## Usage
### GPT3 
this part is write in python3, I run it in spyder so it's needed to source anaconda3 first  
add ```export PATH="/home/Usrname/anaconda3/bin$PATH"``` at the end of ```.bashrc``` file, then source it by ```source ~/.bashrc```  

run this python3 file to get coordinates suggested by GPT3, 
```
test_table_set6.py
```
the ouput coordinates will be stored as 
```
output.npy
```
### Gazebo 
since anaconda3 is unfriendly with ros, you need to unsource conda before running ROS  
first, you need to uncomment ```export PATH="/home/Usrname/anaconda3/bin$PATH"``` at the end of ```.bashrc``` file, then source it by ```source ~/.bashrc```     

Launch banquet3 environment and bring up mobile manipulator
```
roslaunch tamp_perception segbot_ur5_2.launch
```
open another terminal, 
spawn tableware and relocate tableware to the dinning table
```
source ~/catkin_ws/devel/setup.bash
rosrun tamp_percetpion tableware_spawner.py
rosrun tamp_percetpion pick_n_place_2.py
```

