#!/usr/bin/env python
import rospy
import time
import math
import random
from math import cos, sin
from gazebo_msgs.srv import SpawnModel, DeleteModel
from geometry_msgs.msg import Pose, Point, Quaternion

class chair_sampler(object):
    """sample different chair locations and spawn them in the gazebo env
    """
    def __init__(self, num_chair):
        rospy.wait_for_service("/gazebo/spawn_urdf_model")
        self._num_chair = num_chair
        #store sampled positions for all the chairs
        self._positions = []
        self._oriens = []
        #define sample region
        self._x_range = [-7, 7]
        self._y_range = [[4.35, 5.35], [6.8, 7.8]]
        #the minimum distance between two chairs
        self._collision_dist = 0.8
    
    def get_positions(self):
        return self._positions

    def get_oriens(self):
        return self._oriens

    def distance(self, p1, p2):
        return math.sqrt(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))

    def euler_to_quat(self, roll, pitch, yaw):
        cy = cos(yaw * 0.5)
        sy = sin(yaw * 0.5)
        cp = cos(pitch * 0.5)
        sp = sin(pitch * 0.5)
        cr = cos(roll * 0.5)
        sr = sin(roll * 0.5)

        w = cr * cp * cy + sr * sp * sy
        x = sr * cp * cy - cr * sp * sy
        y = cr * sp * cy + sr * cp * sy
        z = cr * cp * sy - sr * sp * cy
        return Quaternion(x, y, z, w)

    def sample_pose(self):
        num_sampled = 0
        pose = []
        while num_sampled < self._num_chair:
            #sample a random number within the x range
            x = random.uniform(self._x_range[0], self._x_range[1])
            #randomly choose to sample on one side of the table
            #y_range = random.choice(self._y_range)
            y_range = self._y_range[0]
            #sample y value
            y = random.uniform(y_range[0], y_range[1])
            #check if sampled point is in collision with other existing points
            is_collision = False
            for p in pose:
                if self.distance(p, [x, y]) < self._collision_dist:
                    is_collision = True
            if is_collision == False:
                num_sampled += 1
                pose.append([x, y])
        self._positions = pose
        
        #sample orientations
        for i in range(0, self._num_chair):
            self._oriens.append(random.uniform((-1)*math.pi, math.pi))

    def spawn_Fork(self):
        for i in range(0, self._num_chair):
            self.sample_pose()
        try:
            spawner = rospy.ServiceProxy("/gazebo/spawn_sdf_model", SpawnModel)
            for i in range(0, len(self._positions)):
                spawner(model_name = 'Fork_'+str(i+1), 
                        model_xml = open("/home/yan/GPT3-testing/Fork1/model.sdf", 'r').read(), 
                        robot_namespace = "/chair", 
                        initial_pose = Pose(position=Point(7.5,0.2,1),orientation=self.euler_to_quat(0, 0, -math.pi/2)), 
                        reference_frame = "world")
            print("Fork added.")
        except rospy.ServiceException as e:
            print("Spawner fails: ", e)

    def spawn_Plate(self):
        for i in range(0, self._num_chair):
            self.sample_pose()
        try:
            spawner = rospy.ServiceProxy("/gazebo/spawn_sdf_model", SpawnModel)
            for i in range(0, len(self._positions)):
                spawner(model_name = 'Plate_'+str(i+1), 
                        model_xml = open("/home/yan/GPT3-testing/Plate5/model.sdf", 'r').read(), 
                        robot_namespace = "/chair", 
                        initial_pose = Pose(position=Point(7.5,0.4,2),orientation=self.euler_to_quat(0, 0, math.pi/2)), 
                        reference_frame = "world")
            print("Plate added.")
        except rospy.ServiceException as e:
            print("Spawner fails: ", e)

    def spawn_Spoon(self):
        for i in range(0, self._num_chair):
            self.sample_pose()
        try:
            spawner = rospy.ServiceProxy("/gazebo/spawn_sdf_model", SpawnModel)
            for i in range(0, len(self._positions)):
                spawner(model_name = 'Spoon_'+str(i+1), 
                        model_xml = open("/home/yan/GPT3-testing/Spoon/model.sdf", 'r').read(), 
                        robot_namespace = "/chair", 
                        initial_pose = Pose(position=Point(7.5,0,2),orientation=self.euler_to_quat(0, 0, -math.pi/2)), 
                        reference_frame = "world")
            print("Spoon added.")
        except rospy.ServiceException as e:
            print("Spawner fails: ", e)

    def spawn_Knife(self):
        for i in range(0, self._num_chair):
            self.sample_pose()
        try:
            spawner = rospy.ServiceProxy("/gazebo/spawn_sdf_model", SpawnModel)
            for i in range(0, len(self._positions)):
                spawner(model_name = 'Knife_'+str(i+1), 
                        model_xml = open("/home/yan/GPT3-testing/Knife4/model.sdf", 'r').read(), 
                        robot_namespace = "/chair", 
                        initial_pose = Pose(position=Point(7.5,-0.2,1),orientation=self.euler_to_quat(0, 0, -math.pi/2)), 
                        reference_frame = "world")
            print("Knife added.")
        except rospy.ServiceException as e:
            print("Spawner fails: ", e)

    def spawn_Cup(self):
        for i in range(0, self._num_chair):
            self.sample_pose()
        try:
            spawner = rospy.ServiceProxy("/gazebo/spawn_sdf_model", SpawnModel)
            for i in range(0, len(self._positions)):
                spawner(model_name = 'Cup_'+str(i+1), 
                        model_xml = open("/home/yan/GPT3-testing/Cup/model.sdf", 'r').read(), 
                        robot_namespace = "/chair", 
                        initial_pose = Pose(position=Point(7.4,-0.4,1),orientation=self.euler_to_quat(0, 0, math.pi/2)), 
                        reference_frame = "world")
            print("Cup added.")
        except rospy.ServiceException as e:
            print("Spawner fails: ", e)

    def delete_all(self):

        try:
            remover = rospy.ServiceProxy("/gazebo/delete_model", DeleteModel)
            for i in range(0, self._num_chair):
                remover(model_name = 'chair_'+str(i+1))
            remover(model_name = 'test_stick')
            print("Items removed.")
        except rospy.ServiceException as e:
            print("Spawner fails: ", e)



def main():
    test = chair_sampler(1)
    test.spawn_Plate()
    test.spawn_Fork() 
    test.spawn_Spoon()
    test.spawn_Knife()
    test.spawn_Cup()
    #time.sleep(3)
    #test.delete_all()
    #test.sample_pose()


if __name__ == '__main__':
    main()
