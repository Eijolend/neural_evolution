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
from random import random
pg.init()

CREEP_START_FOOD = 50
CREEP_FOOD_DECAY = 1
CREEP_FOOD_MAX = 100
WORLD_CANVAS = WORLD_WIDTH, WORLD_HEIGHT = 900,900
WORLD_SIZE = 30,30
NETWORK = [2,4,2]
CREEP_COLOR = 255,0,0
CREEP_NOSE_COLOR = 0,0,255
BLACK = 0,0,0
CREEP_DEAD_COLOR = 169,169,169
CREEP_RADIUS = 10
CREEP_NOSE_RADIUS = 3
CREEP_ACCELERATION = 0.25
CREEP_MAX_SPEED = 5
CREEP_TURN_SPEED = 5
CREEP_EAT_RATE = 1.5
FOOD_GROWTH = 0.005
WORLD_FOOD_MAX = 100
GENERATION_INTERVAL = 900

clock = pg.time.Clock()

world = np.ones(WORLD_SIZE)*5 + np.random.rand(*WORLD_SIZE)*2

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
        self.alive = True

    
    def eat(self):
        i = int(self.pos[0] * WORLD_SIZE[0] / WORLD_WIDTH)
        j = int(self.pos[1] * WORLD_SIZE[1] / WORLD_HEIGHT)
        eat_amount = min(world[i,j],CREEP_EAT_RATE,CREEP_FOOD_MAX - self.food)
        self.food += eat_amount
        world[i,j] -= eat_amount
    
        
    def die(self):
        self.alive = False
    
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
            return
        i = int(self.pos[0] * WORLD_SIZE[0] / WORLD_WIDTH)
        j = int(self.pos[1] * WORLD_SIZE[1] / WORLD_HEIGHT)
        inputs = np.array([world[i,j],self.speed]) #input 1 is color on position, input 2 is current speed
        outputs = self.brain.think(inputs)
        acc = (outputs[0] - 0.5)*2 * CREEP_ACCELERATION
        turn = (outputs[1] - 0.5)*2 * CREEP_TURN_SPEED
        new_speed = self.speed + acc
        self.speed = clamp(0,new_speed,CREEP_MAX_SPEED)
        self.facing = (self.facing + turn) % 360
        self.move()
        
        self.age += 1
    
    def draw(self,screen):
        pos = np.rint(np.array(self.pos)).astype(int)
        if self.alive:
            pg.draw.circle(screen,CREEP_COLOR,pos,CREEP_RADIUS,0)
        else:
            pg.draw.circle(screen,CREEP_DEAD_COLOR,pos,CREEP_RADIUS,0)
        pg.draw.circle(screen,BLACK,pos,CREEP_RADIUS,2)
        phi = radians(self.facing)
        nose_pos = np.rint(pos + 0.6*CREEP_RADIUS * np.array([cos(phi),sin(phi)])).astype(int)
        pg.draw.circle(screen,CREEP_NOSE_COLOR,nose_pos,CREEP_NOSE_RADIUS,0)
        


    




screen = pg.display.set_mode(WORLD_CANVAS)

N=10

mybrains = [brain(NETWORK,[np.random.rand(NETWORK[1],NETWORK[0])*2 - 1,np.random.rand(NETWORK[2],NETWORK[1])*2 - 1]) for i in range(N)]

generation = 1 
myfont = pg.font.SysFont("Arial",20)

def hsv_color(h,s,v): #h 0-1, s 0-1, v 0-1
    return np.floor(np.array(hsv_to_rgb(h,s,v))*255)

def draw_world(world):
    nx,ny = world.shape
    dx = WORLD_WIDTH / nx
    dy = WORLD_HEIGHT / ny
    for x,y in product(range(nx),range(ny)):
        pg.draw.rect(screen,hsv_color(0.33,world[x,y]/WORLD_FOOD_MAX,1),(x*dx,y*dy,dx,dy))
#        pg.draw.rect(screen,hsv_color(120,1,1),(x*dx,y*dy,dx,dy))
    return 
        
while True:
    i=0
    world = np.ones(WORLD_SIZE)*5 + np.random.rand(*WORLD_SIZE)*2
    mycreeps = [creep((random()*WORLD_WIDTH,random()*WORLD_HEIGHT),int(random()*360),br) for br in mybrains]
    while i<GENERATION_INTERVAL:
        i+=1
        for event in pg.event.get():
            if event.type == pg.QUIT: sys.exit()
            
        clock.tick(30)
        
        world = np.minimum(world + np.ones(WORLD_SIZE)*FOOD_GROWTH, np.ones(WORLD_SIZE)*WORLD_FOOD_MAX)
        draw_world(world)
        for cr in mycreeps:
            if cr.alive:
                cr.tick()
            cr.draw(screen)
        gen_text=myfont.render("Generation: %d" % generation,1,(0,0,0))
        screen.blit(gen_text,(0,875))
        pg.display.flip()
    #the values in the following section should be turned into CONSTANTS
    bestcreeps = [mycreeps[i] for i in np.argsort(np.array([cr.age for cr in mycreeps]))[-2:] ]
    mybrains = []
    for cr in bestcreeps:
        old_params = cr.brain.params
        mybrains += [cr.brain]
        for i in range(4):
            varied_params = [old_params[0] + (np.random.rand(*old_params[0].shape)-0.5)*0.2,old_params[1] + (np.random.rand(*old_params[1].shape)-0.5)*0.2]
            mybrains += [brain(NETWORK,varied_params)]
    generation += 1
        

        