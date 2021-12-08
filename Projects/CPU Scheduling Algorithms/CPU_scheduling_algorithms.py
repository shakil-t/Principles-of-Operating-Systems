# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 10:43:09 2018

@author: shakil
"""

from random import shuffle
import pygame
pygame.init()

#colors
aquamarine=(127,255,212)
black=(0,0,0)
cornflowerblue=(100,149,237)
crimson=(220,20,60)
darkgrey=(169,169,169)
gold=(240,230,140)
lavender=(230,230,250)
lightcoral=(240,128,128)
lightyellow=(250,250,210)
maroon=(128,0,0)
mediumslateblue=(123,104,238)
mediumvioletred=(199,21,133)
navy=(0,0,128)
orange=(255,165,0)
paleturquoise=(175,238,239)
royalblue=(65,105,225)
turquoise=(64,224,208)
white=(255,255,255)

background=white
text=black

#for coloring the diagram
colors=[turquoise, mediumvioletred, aquamarine, crimson, lightcoral,
        mediumslateblue, maroon,navy, royalblue, aquamarine, cornflowerblue,
        lavender, mediumslateblue, paleturquoise]

#some variables
display_width=1000
display_height=500
display=pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Scheduling Algorithms")
icon=pygame.image.load("c:/Users/shakil/Downloads/OS.jpg")
pygame.display.set_icon(icon)
display.fill(background)

#fps stands for frames per second
fps=30
clock=pygame.time.Clock()

#font
small=11
medium=25
large=60
small_font=pygame.font.Font("C:/Windows/Fonts/HARLOWSI.TTF", small)
medium_font=pygame.font.Font("C:/Windows/Fonts/HARLOWSI.TTF", medium)
large_font=pygame.font.Font("C:/Windows/Fonts/HARLOWSI.TTF", large)

#block size for mapping the diagram
blocksize=5
cte=20

#some needed stuff
class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

class Heap:
    def __init__(self):
        self.heapList=[]
        self.currentSize=0

    def trickleUp(self,i):
        while(i//2>0):
          if(self.heapList[i]<self.heapList[i//2]):
             temp=self.heapList[i//2]
             self.heapList[i//2]=self.heapList[i]
             self.heapList[i]=temp
          i=i//2

    def insert(self,k):
      self.heapList.append(k)
      self.currentSize=self.currentSize+1
      self.percUp(self.currentSize)

    def trickleDown(self,i):
      while((i*2)<=self.currentSize):
          mc=self.minChild(i)
          if(self.heapList[i]>self.heapList[mc]):
              temp=self.heapList[i]
              self.heapList[i]=self.heapList[mc]
              self.heapList[mc]=temp
          i=mc

    def minChild(self,i):
      if(i*2+1>self.currentSize):
          return i*2
      else:
          if(self.heapList[i*2]<self.heapList[i*2+1]):
              return i*2
          else:
              return i*2+1

    def delMin(self):
      retval=self.heapList[1]
      self.heapList[1]=self.heapList[self.currentSize]
      self.currentSize=self.currentSize-1
      self.heapList.pop()
      self.trickleDown(1)
      return retval

    def buildHeap(self, list):
      i=len(list)//2
      self.currentSize=len(list)
      self.heapList=[0]+list[:]
      while(i>0):
          self.trickleDown(i)
          i=i-1

#first step is to define an object as task
class Task:
    def __init__(self, name, entrance_time, service_time):
        #n, e and s are first letters 
        self.n=name
        self.e=entrance_time
        self.s=service_time
        self.w=0
        self.color=white
    def __repr__(self):
        #it's the old version for formatting strings be careful!
        return '(%s, %s, %s)' % (self.n, self.e, self.s)  

#getting input
def getting_data(number_of_tasks):
    #a list of tasks
    l=[]
    print("Enter these information respectively:")
    print("Name of the task, Entrance Time and Service Time:")
    #i is used for iterating
    i=0
    while(i<number_of_tasks):
        n, e, s=input().split()
        e=int(e)
        s=int(s)
        what_to_do=check_data(l, n, e, s)
        if(what_to_do==2):
            print("Oops, there is a task as same as you entered!")
            print("Please correct the information:")
            number_of_tasks+=1
            i+=1
            continue
        elif(what_to_do==1):
            print("Sorry,this name has been used before!")
            print("Please correct the information:")
            number_of_tasks+=1
            i+=1
            continue
        t=Task(n, e, s)
        l.append(t)
        i+=1
    return l

#checking if data has been entered before
#0 means everything is safe and sound 
#1 means the name has been used before
#2 means it has been used before
def check_data(l, n, e, s):
    check=0
    for j in range(0,len(l)):
            if(l[j].n==n):
                if(l[j].e==e):
                    check=2
                else:
                    check=1
    return check

#choosing the algorithm
def choose_algorithm():
    print("Which algorithm do you want to perform on your data?")
    print("1)FCFS")
    print("2)SPN")
    print("3)SRT")
    print("4)RR")
    algorithm=int(input())
    return algorithm

#before performing any algorithm we have to sort tasks by their entrance time
def sorting_tasks1(l):
    l.sort(key=lambda Task: Task.e)
    return l

def sorting_tasks2(l):
    l.sort(key=lambda Task: Task.s)
    return l

def text_objects(text,color,size):
    if size=="small":
        textSurface=small_font.render(text,True,color)
    elif size=="medium":
        textSurface=medium_font.render(text,True,color)
    elif size=="large":
        textSurface=large_font.render(text,True,color)
    return textSurface,textSurface.get_rect()

def message_to_screen(msg,color,y_displace=0,size="small"):
    textSurf,textRect=text_objects(msg,color,size)
    textRect.center=(display_width/2),(display_height/2)+y_displace
    display.blit(textSurf,textRect)

def introduction():
    introduction=True
    while(introduction):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_c:
                    introduction=False
                if event.type==pygame.K_q:
                    pygame.quit()
                    quit()
        display.fill(background)
        message_to_screen("Scheduling Algorithms", mediumvioletred, 0, size="large")
        message_to_screen("Press C to continue or Q to quit and P to pause if necessary", lightcoral, 55, size="medium")
        pygame.display.update()

def pause():
    pause=True
    while(pause):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_c:
                    show()
                    pause=False
                elif event.key==pygame.K_q:
                    pygame.quit()
                    quit()
        display.fill(white)
        message_to_screen("Paused",navy,0,size="large")
        message_to_screen("Press C to continue or Q to quit",royalblue, 45,size="medium")
        pygame.display.update()

def show():
    display.fill(background)
    shuffle(colors)
    number_of_tasks=int(input("Enter the number of tasks"))
    tasks=getting_data(number_of_tasks)
    algorithm=choose_algorithm()
    if(algorithm==1):
        FCFS(tasks)
        pygame.display.update()
    elif(algorithm==2):
        SPN(tasks)
        pygame.display.update()
    elif(algorithm==3):
        SRT(tasks)
        pygame.display.update()
    elif(algorithm==4):
        q=int(input("Enter the quantum time:"))
        RR(tasks, q)
        pygame.display.update()
    Exit=False
    Over=False
    while not Exit:
            while Over==True:
                display.fill(background)
                message_to_screen("Press C to insert new info or Q to quit", lightyellow, 0,size="medium")
                pygame.display.update()
                
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        Exit=True
                        Over=False
                    if event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_q:
                            Exit=True
                            Over=False
                        if event.key==pygame.K_c:
                            display.fill(background)
                            show()
                            
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    Exit=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_p:
                        pause()
    pygame.display.update() 
    clock.tick(fps)
    pygame.quit()
    quit()
    
def drawDetails(x, y, index, width, wait, height, color, name):
    sub=index-width
    temp1="%d" % sub
    display.blit(small_font.render(temp1, True, text), (x, y+height))
    pygame.draw.rect(display, color, (x, y, width*cte, height), 0)
    temp2="%d" % index
    display.blit(small_font.render(temp2, True, text), (x+width*cte, y+height))
    pygame.draw.rect(display, color, (x, y+height+blocksize*3, blocksize, blocksize), 0)
    name+=":"+str(wait)
    display.blit(small_font.render(name, True, text), (x+blocksize+1, y+height+blocksize*2))

def simpleDraw(x, y, index, width, height, color):
    #wait is extra
    sub=index-width
    temp1="%d" % sub
    display.blit(small_font.render(temp1, True, text), (x, y+height))
    pygame.draw.rect(display, color, (x, y, width*cte, height), 0)
    temp="%d" % index
    display.blit(small_font.render(temp, True, text), (x+width*cte, y+height))

#first come first served algorithm
def FCFS(l):
    #however we sort them but this time is for making sure it's sorted
    l=sorting_tasks1(l)
    service_time=0
    for i in range(0, len(l)):
        service_time+=l[i].s
    startX=10
    startY=10
    height=startY+2*blocksize
    waiting_time=0
    total_time=0
    for i in range(0, len(l)):
        if(total_time<l[i].e):
            startX+=(l[i].e-total_time)*cte
            total_time+=l[i].e-total_time+l[i].s
            for j in range(i+1, len(l)):
                if(l[j].e<total_time):
                    l[j].w=total_time-l[j].e
            drawDetails(startX, startY, total_time, l[i].s, l[i].w, height, colors[i], l[i].n)
            startX+=l[i].s*cte
        else:
            total_time+=l[i].s
            for j in range(i+1, len(l)):
                if(l[j].e<total_time):
                    l[j].w=total_time-l[j].e
            drawDetails(startX, startY, total_time, l[i].s, l[i].w, height, colors[i], l[i].n)
            startX+=l[i].s*cte
    for i in range(0, len(l)):
        waiting_time+=l[i].w
    avgWaiting_time=waiting_time/len(l)
    avgTotal_time=(service_time+waiting_time)/len(l)
    s1="Average Waiting Time: "
    s1+=str(avgWaiting_time)
    s2="Average Total Time: "
    s2+=str(avgTotal_time)
    startX=10
    display.blit(medium_font.render(s2, True, text), (startX, startY+height*3))
    display.blit(medium_font.render(s1, True, text), (startX, startY+height*5))
        
def SPN(l1):
    #however we sort them but this time is for making sure it's sorted
    l1=sorting_tasks1(l1)
    service_time=0
    for i in range(0, len(l1)):
        service_time+=l1[i].s
    startX=10
    startY=10
    height=startY+2*blocksize
    waiting_time=0
    total_time=0
    l2=[]
    counter=0
    while l1 or l2:
        i=0
        while(i<len(l1)):
            if(l1[i].e<=total_time):
                l2.append(l1.pop(i))
            else:
                i+=1
        if l2:
            l2=sorting_tasks2(l2)
            for j in range(0, len(l2)):
                l2[j].w=total_time-l2[j].e
            total_time+=l2[0].s
            drawDetails(startX, startY, total_time, l2[0].s, l2[0].w, height, colors[counter], l2[0].n)
            startX+=l2[0].s*cte
            waiting_time+=l2[0].w
            l2.pop(0)
            counter+=1
        else:
             total_time+=1
             startX+=cte
    avgWaiting_time=waiting_time/counter
    avgTotal_time=(service_time+waiting_time)/counter
    s1="Average Waiting Time: "
    s1+=str(avgWaiting_time)
    s2="Average Total Time: "
    s2+=str(avgTotal_time)
    startX=10
    display.blit(medium_font.render(s2, True, text), (startX, startY+height*3))
    display.blit(medium_font.render(s1, True, text), (startX, startY+height*5))
    
def SRT(l1):
    l1=sorting_tasks1(l1)
    service_time=0
    for i in range(0, len(l1)):
        service_time+=l1[i].s
        #just for this method
        l1[i].color=colors[i]
    startX=10
    startY=10
    height=startY+blocksize*2
    #just for this method
    width=1
    waiting_time=0
    total_time=0
    l2=[]
    l3=[]
    while l1 or l2:
        i=0
        while(i<len(l1)):
            if(l1[i].e<=total_time):
                l2.append(l1.pop(i))
            else:
                i+=1
        if l2:
            l2=sorting_tasks2(l2)
            total_time+=1
            l2[0].s-=1
            simpleDraw(startX, startY, total_time, width, height, l2[0].color)
            startX+=width*cte
            for j in range(1, len(l2)):
                l2[j].w+=1
            if(l2[0].s<=0):
                l3.append(l2.pop(0))
        else:
             total_time+=1
             startX+=cte
    startX=10
    for k in range(0, len(l3)):
        #:D
        waiting_time+=l3[k].w
        #now lets get back to...
        pygame.draw.rect(display, l3[k].color, (startX, startY+height+blocksize*3, blocksize, blocksize), 0)
        name=l3[k].n
        name+=":"+str(l3[k].w)
        display.blit(small_font.render(name, True, text), (startX+blocksize+1, startY+height+blocksize*2))
        startX+=blocksize*cte
    avgWaiting_time=waiting_time/len(l3)
    avgTotal_time=(service_time+waiting_time)/len(l3)
    s1="Average Waiting Time: "
    s1+=str(avgWaiting_time)
    s2="Average Total Time: "
    s2+=str(avgTotal_time)
    startX=10
    display.blit(medium_font.render(s2, True, text), (startX, startY+height*3))
    display.blit(medium_font.render(s1, True, text), (startX, startY+height*5))
    
def RR(l1,q):
    l1=sorting_tasks1(l1)
    service_time=0
    for i in range(0, len(l1)):
        service_time+=l1[i].s
        l1[i].color=colors[i]
    startX=10
    startY=10
    height=startY+blocksize*2
    waiting_time=0
    total_time=0
    #just for this method
    waiting_time=0
    total_time=0
    l2=[]
    while l1: 
        i=0
        while(i<len(l1)):
            if(total_time<l1[0].e):
                startX+=(l1[0].e-total_time)*cte
                total_time+=l1[0].e-total_time
                if(l1[0].s>=q):
                    l1[0].s-=q
                    total_time+=q
                    for j in range(1, len(l1)):
                        if(l1[j].e<=total_time):
                            l1[j].w+=q
                    simpleDraw(startX, startY, total_time, q, height, l1[0].color)
                    startX+=q*cte
                    if(l1[0].s<=0):
                        l2.append(l1.pop(0))
                    else:
                        i+=1
                else:
                    total_time+=l1[0].s
                    for j in range(1, len(l1)):
                        if(l1[j].e<=total_time):
                            l1[j].w+=l1[i].s
                    simpleDraw(startX, startY, total_time, l1[0].s, height, l1[0].color)
                    startX+=l1[0].s*cte
                    l1[0].s=0
                    l2.append(l1.pop(0))
            else:
                if(l1[i].e<=total_time):
                    if(l1[i].s>=q):
                        l1[i].s-=q
                        total_time+=q
                        for j in range(0, len(l1)):
                            if(i!=j and l1[j].e<=total_time):
                                l1[j].w+=q
                        simpleDraw(startX, startY, total_time, q, height, l1[i].color)
                        startX+=q*cte
                        if(l1[i].s<=0):
                            l2.append(l1.pop(i))
                        else:
                            i+=1
                    else:
                        total_time+=l1[i].s
                        for j in range(0, len(l1)):
                            if(i!=j and l1[j].e<=total_time):
                                l1[j].w+=l1[i].s
                        simpleDraw(startX, startY, total_time, l1[i].s, height, l1[i].color)
                        startX+=l1[i].s*cte
                        l1[i].s=0
                        l2.append(l1.pop(i))
                else:
                    i=0   
    startX=10
    for k in range(0, len(l2)):
    #:D
        waiting_time+=l2[k].w
        #now lets get back to...
        pygame.draw.rect(display, l2[k].color, (startX, startY+height+blocksize*3, blocksize, blocksize), 0)
        name=l2[k].n
        name+=":"+str(l2[k].w)
        display.blit(small_font.render(name, True, text), (startX+blocksize+1, startY+height+blocksize*2))
        startX+=blocksize*cte
    avgWaiting_time=waiting_time/len(l2)
    avgTotal_time=(service_time+waiting_time)/len(l2)
    s1="Average Waiting Time: "
    s1+=str(avgWaiting_time)
    s2="Average Total Time: "
    s2+=str(avgTotal_time)
    startX=10
    display.blit(medium_font.render(s2, True, text), (startX, startY+height*3))
    display.blit(medium_font.render(s1, True, text), (startX, startY+height*5))

introduction()
show()
