# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 21:51:12 2017

@author: Julius
"""

import sys
import pygame as pg
import numpy as np
from itertools import product
from colorsys import hsv_to_rgb
from math import radians, sin, cos
pg.init()

CREEP_START_FOOD = 50
CREEP_FOOD_DECAY = 1
WORLD_SIZE = WORLD_WIDTH, WORLD_HEIGHT = 900,900
NETWORK = [1,4,2]
CREEP_COLOR = 255,0,0
CREEP_NOSE_COLOR = 0,0,255
BLACK = 0,0,0
CREEP_RADIUS = 10
CREEP_NOSE_RADIUS = 3
CREEP_ACCELERATION = 0.5
CREEP_MAX_SPEED = 10
CREEP_TURN_SPEED = 5

def sig(x):
    return 1/(1+np.exp(-x))

def clamp(floor,n,ceil):
    return min(max(floor,n),ceil)

class brain: #this is a simple neural network with 1 hidden layer
    def __init__ (self,network,params):
        self.network = network
        self.params = params
        
    def think(self,inputs):
        hidden = sig(np.dot(self.params[0],inputs))
        return sig(np.dot(self.params[1],hidden))
    
class creep:
    def __init__(self,pos,facing,brain):
        #install brain
        self.brain = brain
        #initialize body
        self.age = 0
        self.pos = pos
        self.facing = facing #0-359
        self.speed = 0.
        self.food = CREEP_START_FOOD
#        self.alive = True

    
    def eat(self):
        pass
        
    def die(self):
        pass
    
    def move(self):
        x,y = self.pos
        phi = radians(self.facing)
        x += self.speed * cos(phi)
        y += self.speed * sin(phi)
        x = x % WORLD_WIDTH
        y = y % WORLD_HEIGHT
        self.pos = x,y
    
    def tick(self):
        self.eat()
        self.food -= CREEP_FOOD_DECAY
        if self.food < 0:
            self.die()
#            return
        inputs = np.random.rand(1)
        outputs = self.brain.think(inputs)
        acc = (outputs[0] - 0.5)*2 * CREEP_ACCELERATION
        turn = (outputs[1] - 0.5)*2 * CREEP_TURN_SPEED
        new_speed = self.speed + acc
        self.speed = clamp(-CREEP_MAX_SPEED,new_speed,CREEP_MAX_SPEED)
        self.facing = (self.facing + turn) % 360
        self.move()
        
        self.age += 1
    
    def draw(self,screen):
        pos = np.rint(np.array(self.pos)).astype(int)
        pg.draw.circle(screen,CREEP_COLOR,pos,CREEP_RADIUS,0)
        pg.draw.circle(screen,BLACK,pos,CREEP_RADIUS,2)
        phi = radians(self.facing)
        nose_pos = np.rint(pos + 0.6*CREEP_RADIUS * np.array([cos(phi),sin(phi)])).astype(int)
        pg.draw.circle(screen,CREEP_NOSE_COLOR,nose_pos,CREEP_NOSE_RADIUS,0)
        


    

clock = pg.time.Clock()

size = width, height = 900,900
black = 0,0,0

screen = pg.display.set_mode(size)

N=10

mybrains = [brain(NETWORK,[np.random.rand(NETWORK[1],NETWORK[0])*2 - 1,np.random.rand(NETWORK[2],NETWORK[1])*2 - 1]) for i in range(N)]
mycreeps = [creep((450,450),0,brain) for brain in mybrains]


def hsv_color(h,s,v): #h 0-1, s 0-1, v 0-1
    return np.floor(np.array(hsv_to_rgb(h,s,v))*255)

def draw_world(world):
    nx,ny = world.shape
    dx = width / nx
    dy = height / ny
    for x,y in product(range(nx),range(ny)):
        pg.draw.rect(screen,hsv_color(0.33,world[x,y],0.9),(x*dx,y*dy,dx,dy))
#        pg.draw.rect(screen,hsv_color(120,1,1),(x*dx,y*dy,dx,dy))
    return 
        
world = np.random.rand(30,30)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT: sys.exit()
        
    clock.tick(30)

    draw_world(world)
    for creep in mycreeps:
        creep.tick()
        creep.draw(screen)
    pg.display.flip()
