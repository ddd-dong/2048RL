import random
import copy
# import pygame
# from pygame.locals import QUIT
import os
import time
import tkinter as tk

def key_w_judge():
  
  for x in range(0,4):
      for y in range(1,4):
        now_num=map[y][x]
        available=0
        map[y][x]=0
        for i in range(y,-1,-1):
          if map[i][x]==0:
            
            available=i
        ###
        
        map[available][x]=now_num
        if available==0:
          pass
        elif map[available-1][x]==map[available][x] and merge_yn[available-1][x]==0:
          
          merge_yn[available-1][x]=1
          map[available][x]=0
          map[available-1][x]=now_num*2
  
 

def key_s_judge():
  
  for x in range(0,4):
      for y in range(2,-1,-1):
        now_num=map[y][x]
        available=0
        map[y][x]=0
        for i in range(y,4):
          if map[i][x]==0:
            
            available=i
      ##
        map[available][x]=now_num
        if available==3:
          pass
        elif map[available+1][x]==map[available][x] and merge_yn[available+1][x]==0:
          merge_yn[available+1][x]=1
          map[available][x]=0
          map[available+1][x]=now_num*2

def key_a_judge():
  
  for y in range(0,4):
      for x in range(1,4):
        now_num=map[y][x]
        available=0
        map[y][x]=0
        for i in range(x,-1,-1):
          if map[y][i]==0:
            
            available=i
        ###
        
        map[y][available]=now_num
        if available==0:
          pass
        elif map[y][available-1]==map[y][available] and merge_yn[y][available-1]==0:
          merge_yn[y][available-1]=1
          map[y][available]=0
          map[y][available-1]=now_num*2
  
def key_d_judge():
  
  for y in range(0,4):
      for x in range(2,-1,-1):
        now_num=map[y][x]
        available=0
        map[y][x]=0
        for i in range(x,4):
          if map[y][i]==0:
          
            available=i
            
        ###
        map[y][available]=now_num
        if available==3:
          pass
        elif map[y][available+1]==map[y][available] and merge_yn[y][available+1]==0:
          merge_yn[y][available+1]=1
          map[y][available]=0
          map[y][available+1]=now_num*2
 
available_x=[]
available_y=[]

merge_yn=[[0,0,0,0],
          [0,0,0,0],
          [0,0,0,0],
          [0,0,0,0]]

map=[[0,0,0,0],
     [0,0,0,0],
     [0,0,0,0],
     [0,0,0,0]]
judge_map=[[0,0,0,0],
           [0,0,0,0],
           [0,0,0,0],
           [0,0,0,0]]
rx=random.randint(0,1)
ry=random.randint(0,3)
  
map[ry][rx]=2
rx=random.randint(2,3)
ry=random.randint(0,3)
map[ry][rx]=2

game_continue=True
while(game_continue):
  

  for y in range(0,3):
    for x in range(0,3):
      merge_yn[y][x]=0
  
  judge_map=copy.deepcopy(map)
  for i in range(4):
    print(map[i])
  key=input()
  
  if key=="w":
    key_w_judge()
      
 
  elif key=="s":
    key_s_judge()
     
  
  elif key=="a":
    key_a_judge()
     
        ###
  elif key=="d":
    key_d_judge()
   
  else:
    print("無效輸入")
    continue
  

  
  if judge_map==map:
    continue
    #
  available_x=[]
  available_y=[]
  for y in range(0,4):
    for x in range(0,4):
      if map[y][x]==0:
        available_x.append(x)
        available_y.append(y)
  j=random.randint(0,len(available_x)-1)
  
  map[available_y[j]][available_x[j]]=2