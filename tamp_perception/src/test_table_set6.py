# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 15:54:15 2021

@author: Zetong
"""


import openai
import numpy as np
import re
import matplotlib.pyplot as plt

f = open('openai_api_key.txt',"r")   
key = f.read()   
f.close() 

openai.api_key = key

def Q_A (question):

    response = openai.Completion.create(
        engine="davinci",
        # engine="curie",
      prompt = question + ''+ "\nA:",
      temperature=0,
      max_tokens=100,
      top_p=1,
      frequency_penalty=0.0,
      presence_penalty=0.0,
      # response_lenght=1,
       stop=["\n"]
    )
    # print(response)   
    choices = response['choices']
    choices = choices[0]
    text = choices['text']
    print(text+'\n')
    return text
# get 2 dustabce constrains
def Constrains (objects,index):
    if index == 0:
        # question_2 = ("what's the proper distance between the " + objects[index] + " and plate on the dining table in centimeter?"
        #     "/n")
        question_2 = ("what's the distance between the " + objects[index] + " and plate on the dining table in centimeter?"
                "/n")
    else:
        question_2 = ("what's the distance between the " + objects[index] + " and the "+ objects[index-1] + " on the dining table in centimeter?"
                "/n")
        
    response_2 = Q_A (question_2)
    temp = re.findall(r"\d+\.?\d*",response_2)
    distance_2 = np.fromstring(temp[0], dtype=float, sep=' ')
    
    # question_3 = ("how far should the " + objects[index] + " be placed away from the edge of dining table in centimeter?"
    #        "/n")
    
    question_3 = ("what should the distance between the " + objects[index] + " and the edge of dining table in centimeter?"
           "/n")
    response_3 = Q_A (question_3)
    temp = re.findall(r"\d+\.?\d*",response_3)
    distance_3 = np.fromstring(temp[0], dtype=float, sep=' ')
    if index == 0:
        distance_2 = distance_2 + 10
    else:
        distance_2 = distance_2 + 2
    return np.array([distance_2, distance_3])
    

objects = ['plate','spoon','fork','table knife','cup']
num = len(objects)
left_list = []; 
right_list = []; 

for i in range(1,num): 
    question = ("what's the relative position of " + objects[i] + " and the plate on the dining table?"
                "/n")
    response = Q_A (question)
    if 'left' in response:
        left_list.append(objects[i])
    if 'right' in response:
        right_list.append(objects[i])
        
for j in range(len(right_list)):
    for i in range(len(right_list)-1): 
        question = ("what's the relative position of " + right_list[i+1] + " and the " + right_list[i] + " on the dining table?"
                    "/n")
        response = Q_A (question)
        if "left" in response:
            temp = right_list[i]
            right_list[i] = right_list[i+1]
            right_list[i+1] = temp
            
for j in range(len(left_list)):
    for i in range(len(left_list)-1): 
        question = ("what's the relative position of " + right_list[i+1] + " and the " + right_list[i] + " on the dining table?"
                    "/n")
        response = Q_A (question)
        if "left" in response:
            temp = right_list[i]
            right_list[i] = right_list[i+1]
            right_list[i+1] = temp

left_list.append('plate')
left_list.extend(right_list)
objects = left_list
print(objects)
#%%
# pre-define Plate position


left_objects = objects[ 0 : objects.index('plate') ]
right_objects = objects[ objects.index('plate') + 1 : len(objects)]

Pos_plate = np.array([50,30])
Pos_select = np.array([50,30])
Pos_index = np.zeros([len(objects),2])

# objects = right_objects

def Pos_right (objects,left_right):
    Pos_plate = np.array([50,30])
    Pos_select = np.array([50,30])
    Pos_index = np.zeros([len(objects),2])
    
    for i in range(0,len(objects)):
        
        if i > 0:
            Pos_plate = Pos_select[0]
            
        flag_array_1 = np.zeros([100,60])
        # # right: 1, left: 0
        # if i > objects.index('plate'):
        #     left_right = 1
        # elif i < objects.index('plate'):
        #     left_right = 0
        
        
        temp = Constrains(objects,i)
        distance_2 = temp[0]
        distance_3 = temp[1]
    
        for x in range(100):
            for y in range(60):    
                Pos_obj = np.array([x,y])
                Pos_flag_1 = 0
                Pos_flag_2 = 0
                Pos_flag_3 = 0
                 
                if Pos_obj[0] < Pos_plate[0]:
                    left_right_true = 0
                elif Pos_obj[0] > Pos_plate[0]:
                    left_right_true = 1   
                if left_right == left_right_true:
                    Pos_flag_1 = 1
        
                # ture_dist = np.linalg.norm(Pos_plate-Pos_obj, 2)
                
                ture_dist = np.abs(Pos_plate[0] - Pos_obj[0])
                error = np.abs(ture_dist - distance_2)
                
                if error < 5:
                    Pos_flag_2 = 1
                        
                ture_dist = np.min([Pos_obj[1],60-Pos_obj[1]])
                if ture_dist > distance_3:
                    Pos_flag_3 = 1
                    
                if Pos_flag_1*Pos_flag_2*Pos_flag_3 == 1:
                    flag_array_1[x,y] = 1
                    
        index = np.argwhere(flag_array_1  == 1)
        
        # Pos_select = index[ np.random.choice(index.shape[0]-1) ] 
        # Pos_index[i] = Pos_select
        
        a = np.min(index[:,0])
        b = np.max(index[:,0])
        c = np.min(index[:,1])
        d = np.max(index[:,1])
        mean = np.array([ (a+b)/2, (c+d)/2])
        conv = np.array([[ abs(a-b), 0.0],        # 协方差矩阵
                          [0.0, abs(c-d)]])
        Pos_select = np.random.multivariate_normal(mean=mean, cov=conv, size=1)
        
        Pos_index[i] = Pos_select[0]
            
    return Pos_index

left_right = 1
Pos_index_1 =  Pos_right (right_objects,left_right)
print(Pos_index_1)

left_right = 0
Pos_index_2 =  Pos_right (left_objects,left_right)
print(Pos_index_2)

Pos_index = np.vstack((Pos_index_2,Pos_plate,Pos_index_1))
x = Pos_index[:,0]
y = Pos_index[:,1
              ]


plt.plot(x, y, 'ro')
plt.xlim(0, 100)
plt.ylim(0, 60)
plt.show()

# Pos_index = Pos_right(right_objects)
#     plt.figure()
#     for x in range(100):
#         for y in range(60):   
#             if flag_array_1[x,y]== 1:
#                 plt.plot([x],[y],marker='o', c='b')
#             else:
#                 plt.plot([x],[y],marker='o', c='r')
#%%
new_Pose = (Pos_index + np.array([-50,395]) )/100 



new_Pose[objects.index('fork')] = new_Pose[objects.index('fork')] + np.array([0,0.1])
new_Pose[objects.index('spoon')] = new_Pose[objects.index('spoon')] + np.array([0,0.1])
new_Pose[objects.index('table knife')] = new_Pose[objects.index('table knife')] + np.array([0,0.1])


output = 0*new_Pose
output[0] = new_Pose[objects.index('plate')]
output[1] = new_Pose[objects.index('fork')]
output[2] = new_Pose[objects.index('spoon')]
output[3] = new_Pose[objects.index('table knife')]
output[4] = new_Pose[objects.index('cup')]

np.save('output.npy',output)

#a = np.load('output.npy')
#a = a.tolist()
