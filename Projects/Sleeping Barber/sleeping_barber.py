# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 20:10:45 2018

@author: shakil
"""

import pygame 
pygame.init()
from threading import Thread, Lock, Event
import time

ME=Lock()

crimson=(220,20,60)
lavender=(230,230,250)
navy=(0,0,128)
white=(255, 255, 255)
background=white

display_width=500
display_heigth=300

display=pygame.display.set_mode((display_width, display_heigth))
pygame.display.set_caption("Barber Shop")
icon=pygame.image.load("D:/University/Operating Systems/Operating Systems Project/barber shop.jpg")
pygame.display.set_icon(icon)
display.fill(background)
pygame.display.update()

#fps stands for frames per second
fps=30
clock=pygame.time.Clock()

class BarberShop:
    customers=0
    def __init__(self, barber, chairs):
        self.barber=barber
        self.chairs=chairs
    def opening_the_shop(self):
        display.fill(lavender)
        pygame.display.update()
        start=Thread(target = self.barber_goes_to_work)
        start.start()
    def barber_goes_to_work(self):
        while(True):
            ME.acquire()
            if(self.customers>0):
                self.customers-=1
                ME.release()
                self.barber.hair_cut()
            else:
                ME.release()
                self.barber.sleep()
    def enter(self):
        ME.acquire()
        if(self.customers==self.chairs):
            print("Sorry, there is no empty chair!")
            ME.release()
        else:
            self.customers+=1
            ME.release()
            self.barber.wake_up()

class Barber:
    #Creating an event for commiunication between threads
    working=Event()
    def sleep(self):
         display.fill(navy)
         pygame.display.update()
         self.working.wait()
    def wake_up(self):
        display.fill(lavender)
        pygame.display.update()
        time.sleep(1)
        self.working.set()
    def hair_cut(self):
        display.fill(crimson)
        pygame.display.update()
        time.sleep(1)
        self.working.clear()

def barber_shop(chairs):
    barber=Barber()
    shop=BarberShop(barber, chairs)
    shop.opening_the_shop()
    Exit=False
    while not Exit:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                Exit=True
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_c:
                    shop.enter()
    pygame.display.update() 
    clock.tick(fps)
    pygame.quit()
    quit()

chairs=int(input("Number of chairs in the waiting room:"))
barber_shop(chairs)
