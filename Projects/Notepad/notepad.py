# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 15:52:18 2018

@author: shakil
"""

import pygame
import sys
import os
import math
from pygame.locals import*
pygame.init()

#colors
black=(0,0,0)
darkgrey=(169,169,169)
gold=(240,230,140)
lavender=(230,230,250)
lightcoral=(240,128,128)
lightyellow=(250,250,210)
maroon=(128,0,0)
mediumvioletred=(199,21,133)
navy=(0,0,128)
orange=(255,165,0)
paleturquoise=(175,238,239)
royalblur=(65,105,225)
white=(255,255,255)

backgroundColor=white
textColor=maroon
cursorColor=gold

#some variables
inputDisplay_width=640
inputDisplay_height=480
#fps stands for frames per second
fps=30
textHeight=20
startX=0
startY=0
#directions
down="down"
left="left"
right="right"
up="up"
#font
font=pygame.font.Font("C:/Windows/Fonts/HARLOWSI.TTF", textHeight)

def notepad(screen):
    lineNumber=0
    newChar=''
    typeChar=False
    textString=''
    stringList=[]
    stringList.append(textString)
    deleteKey=False
    returnKey=False
    directionKey=False
    insertPoint=0
    camerax=0
    cameray=0
    mouseClicked=False
    mouseX=0
    mouseY=0
    cursorRect=getCursorRect(startX, startY+(textHeight+(textHeight/4)),
                             font, camerax, cameray)
    while True:
        camerax, cameray=adjustCamera(stringList, lineNumber, insertPoint,
                                      cursorRect, font, camerax, cameray,
                                      inputDisplay_width, inputDisplay_height)
        newChar, typeChar, deleteKey, returnKey, directionKey,
        inputDisplay_width, inputDisplay_height, mouseX, mouseY,
        mouseClicked=getInput(inputDisplay_width, inputDisplay_height)
        if(newChar=='escape'):
            StringList=saveAndLoadScreen(StringList, inputDisplay_width,
                                         inputDisplay_height, screen, font)
            newChar=False
            insertPoint=0
            lineNumber=0
        
        stringList, lineNumber, insertPoint, cursorRect=displayText(font,newChar,
                                                                    typeChar,
                                                                    stringList,
                                                                    deleteKey,
                                                                    returnKey,
                                                                    lineNumber,
                                                                    insertPoint,
                                                                    directionKey,
                                                                    camerax, cameray,
                                                                    cursorRect,
                                                                    inputDisplay_width,
                                                                    inputDisplay_height,
                                                                    screen,
                                                                    mouseClicked,
                                                                    mouseX, mouseY)

def displayText(mainFont, newChar, typeChar, mainList, deleteKey, returnKey, lineNumber,
                insertPoint, directionKey, camerax, cameray, cursorRect, windowWidth,
                windowHeight, displaySurf, mouseClicked, mouseX, mouseY):
    if(returnKey):
        firstString=getStringAtInsertPoint(mainList, lineNumber, insertPoint)
        secondString=getStringAfterInsertPoint(mainList, lineNumber, insertPoint)
        mainList[lineNumber]=firstString
        mainList.insert(lineNumber+1, secondString)
        lineNumber+=1
        returnKey= False
        insertPoint=0
        cursorRect.x=startX
        stringRect=getStringRectAtInsertPoint(mainList, lineNumber, insertPoint,
                                              mainFont, camerax, cameray)
        cursorRect.y=stringRect.top
        
    elif(mouseClicked):
        insertPoint, lineNumber, cursorRect=setCursorToClick(mainList, cursorRect, 
                                                             mainFont, camerax,
                                                             cameray, mouseX,
                                                             mouseY)
    elif(directionKey):
        if(directionKey==left):
            if(lineNumber==0):
                if(insertPoint>0):
                    insertPoint-=1
                    stringRect=getStringRectAtInsertPoint(mainList, lineNumber,
                                                          insertPoint, mainFont,
                                                          camerax, cameray)
                    cursorRect.x=stringRect.right
                    cursorRect.y=startY
            elif(lineNumber>0):
                if(insertPoint==0):
                    lineNumber-=1
                    insertPoint=len(mainList[lineNumber])
                    stringRect=getStringRectAtInsertPoint(mainList, lineNumber,
                                                          insertPoint, mainFont,
                                                          camerax, cameray)
                    cursorRect.x=stringRect.right
                    cursorRect.y=stringRect.top   
                elif(insertPoint>0):
                    insertPoint-=1
                    stringRect=getStringRectAtInsertPoint(mainList, lineNumber,
                                                          insertPoint, mainFont,
                                                          camerax, cameray)
                    if(insertPoint==0):
                        cursorRect.x=startX
                        cursorRect.y=stringRect.top
                    else:
                        cursorRect.x = stringRect.right
                        cursorRect.y = stringRect.top
        elif(directionKey==right):
            if(insertPoint<len(mainList[lineNumber])):
                insertPoint+=1
                stringRect=getStringRectAtInsertPoint(mainList, lineNumber, insertPoint,
                                                      mainFont, camerax, cameray)
                cursorRect.x=stringRect.right
                cursorRect.y=stringRect.top
            elif(insertPoint>=len(mainList[lineNumber])):
                if(len(mainList)>(lineNumber+1)):
                    lineNumber+=1
                    insertPoint=0
                    stringRect=getStringRectAtInsertPoint(mainList, lineNumber,
                                                          insertPoint, mainFont,
                                                          camerax, cameray)
                    cursorRect.x=stringRect.right
                    cursorRect.y=stringRect.top
                    
        elif(directionKey==up):
            if(lineNumber>0):
                if(insertPoint==0):
                    lineNumber-=1
                    stringRect=getStringRectAtInsertPoint(mainList, lineNumber,
                                                          insertPoint, mainFont,
                                                          camerax, cameray)
                    cursorRect.x=startX
                    cursorRect.y=stringRect.top
                elif(insertPoint>len(mainList[lineNumber-1])):
                    lineNumber-=1
                    insertPoint=len(mainList[lineNumber])
                    stringRect=getStringRectAtInsertPoint(mainList, lineNumber,
                                                          insertPoint, mainFont,
                                                          camerax, cameray)
                    cursorRect.x=stringRect.right
                    cursorRect.y=stringRect.top
                elif(insertPoint<=len(mainList[lineNumber-1])):
                    lineNumber-=1
                    stringRect=getStringRectAtInsertPoint(mainList, lineNumber,
                                                          insertPoint, mainFont,
                                                          camerax, cameray)
                    cursorRect.x=stringRect.right
                    cursorRect.y=stringRect.top
        elif(directionKey==down):
            if(lineNumber+1<len(mainList)):
                if(insertPoint==0):
                    lineNumber+=1
                    stringRect=getStringRectAtInsertPoint(mainList, lineNumber,
                                                          insertPoint, mainFont,
                                                          camerax, cameray)
                    cursorRect.x=startX
                    cursorRect.y=stringRect.top
                elif(insertPoint>len(mainList[lineNumber+1])):
                    lineNumber+=1
                    insertPoint=len(mainList[lineNumber])
                    stringRect=getStringRectAtInsertPoint(mainList, lineNumber,
                                                          insertPoint, mainFont,
                                                          camerax, cameray)
                    cursorRect.x=stringRect.right
                    cursorRect.y=stringRect.top
                elif(insertPoint<=len(mainList[lineNumber+1])):
                    lineNumber+=1
                    stringRect=getStringRectAtInsertPoint(mainList, lineNumber,
                                                          insertPoint, mainFont,
                                                          camerax, cameray)
                    cursorRect.x=stringRect.right
                    cursorRect.y=stringRect.top
                    
    elif(typeChar):
        string=mainList[lineNumber]
        stringList=list(string)
        stringList.insert(insertPoint, newChar)
        newString="".join(stringList)
        mainList[lineNumber]=newString
        typeChar=False
        if(len(newString)>len(string) and newChar!="    "):
            insertPoint+=1
            stringRect=getStringRectAtInsertPoint(mainList, lineNumber, insertPoint,
                                                  mainFont, camerax, cameray)
            cursorRect.x=stringRect.right
            cursorRect.y=stringRect.top
        elif(newChar=="    "):
            insertPoint+=4
            stringRect=getStringRectAtInsertPoint(mainList, lineNumber, insertPoint,
                                                  mainFont, camerax, cameray)
            cursorRect.x=stringRect.right
            cursorRect.y=stringRect.top
    elif(deleteKey):
        if(insertPoint>0):
            firstString=getStringAtInsertPoint(mainList, lineNumber, insertPoint)
            secondString=getStringAfterInsertPoint(mainList, lineNumber, insertPoint)
            stringList=list(firstString)
            del stringList[insertPoint-1]
            string="".join(stringList)
            string+=secondString
            mainList[lineNumber]=string
            deleteKey=False
            insertPoint-=1
            stringRect=getStringRectAtInsertPoint(mainList, lineNumber, insertPoint,
                                                  mainFont, camerax, cameray)
            cursorRect.x=stringRect.right
            cursorRect.y=stringRect.top
        elif(insertPoint<=0):
            if(lineNumber>0):
                string=getStringAfterInsertPoint(mainList, lineNumber, insertPoint)
                del mainList[lineNumber]
                lineNumber-=1
                mainList[lineNumber]+=string
                deleteKey=False
                insertPoint=len(mainList[lineNumber])-len(string)
                stringRect=getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)                
                cursorRect.x=stringRect.right
                cursorRect.y=stringRect.top
    else:
        stringRect=getStringRectAtInsertPoint(mainList, lineNumber, insertPoint,
                                              mainFont, camerax, cameray)
        if(insertPoint==0):
            cursorRect.x=startX
        elif(insertPoint>0):
            cursorRect.x=stringRect.right
        if(lineNumber==0):
            cursorRect.y=startY
        elif(lineNumber>0):
            cursorRect.y=stringRect.top
        else:
            cursorRect.x=stringRect.right
    if(cursorRect.left>=startX):
        if(cursorRect.right<=windowWidth):
            if(cursorRect.top>=startY):
                if(cursorRect.bottom<=(windowHeight-startY)):
                    blitAll(mainList, mainFont, camerax, cameray, cursorRect, displaySurf)
    return mainList, lineNumber, insertPoint, cursorRect

def blitAll(mainList, mainFont, camerax, cameray, cursorRect, displaySurf):
    displaySurf.fill(backgroundColor)
    i=0
    for string in mainList:  
        stringRender=mainFont.render(string, True, textColor, backgroundColor)
        stringRect=stringRender.get_rect()
        stringRect.x=startX-camerax
        stringRect.y=startY+(i*(textHeight+(textHeight/4)))-cameray
        displaySurf.blit(stringRender, stringRect)
        i+=1
    drawCursor(mainFont, cursorRect, displaySurf)

def adjustCamera(mainList, lineNumber, insertPoint, cursorRect, mainFont, camerax,
                 cameray, windowWidth, windowHeight):
    stringRect=getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont,
                                          camerax, cameray)
    
    if((stringRect.right+cursorRect.width)>windowWidth):
        camerax+=(stringRect.right+cursorRect.width)-windowWidth  
    elif(cursorRect.left<startX):
        camerax-=(-1)*(cursorRect.left)
    if(stringRect.bottom>windowHeight):
        cameray+=stringRect.bottom-windowHeight
    elif(stringRect.top<0):
        cameray-=(-1)*(stringRect.top)
    if(insertPoint==0):
        camerax=0
    if(lineNumber==0):
        cameray=0
    return camerax, cameray
    
def drawCursor(mainFont, cursorRect, displaySurf):
    cursor=mainFont.render('l', True, cursorColor, cursorColor)
    displaySurf.blit(cursor, cursorRect)
    
def getInput(windowWidth, windowHeight):
    newChar=False
    typeChar=False
    deleteKey=False
    returnKey=False
    directionKey=False
    mouseX=0
    mouseY=0
    mouseClicked=False
    for event in pygame.event.get():
        if(event.type==QUIT):
            pygame.quit()
            sys.exit()
        elif(event.type==KEYDOWN):
            if(event.key==K_BACKSPACE):
                deleteKey=True
            elif(event.key==K_ESCAPE):
                newChar="escape"
            elif(event.key==K_RETURN):
                returnKey=True
            elif(event.key==K_TAB):
                newChar="    "
                typeChar=True
            elif(event.key==K_LEFT):
                directionKey=left
            elif(event.key==K_RIGHT):
                directionKey=right
            elif(event.key==K_UP):
                directionKey=up
            elif(event.key==K_DOWN):
                directionKey=down
            else:
                newChar=event.unicode
                typeChar=True
        elif(event.type==VIDEORESIZE):
            screen=pygame.display.set_mode(event.dict['size'],RESIZABLE)
            windowWidth=event.dict['w']
            windowHeight=event.dict['h']
            screen.fill(white)
            screen.convert()
            pygame.display.update()
        elif(event.type==MOUSEBUTTONDOWN):
            mouseX, mouseY=event.pos
            mouseClicked=True
    return newChar, typeChar, deleteKey, returnKey, directionKey, windowWidth, windowHeight, mouseX, mouseY, mouseClicked

def getStringRect(string, lineNumber, camerax, cameray):
    stringRect=string.get_rect()
    stringRect.x=startX-camerax
    stringRect.y=startY+(lineNumber*(textHeight+(textHeight/4)))-cameray
    return stringRect

def getStringAtInsertPoint(mainList, lineNumber, insertPoint):
    string=mainList[lineNumber]
    stringList=list(string)
    newStringList=stringList[0:insertPoint]
    newString="".join(newStringList)
    return newString

def getStringAfterInsertPoint(mainList, lineNumber, insertPoint):
    string=mainList[lineNumber]
    stringList=list(string)
    newStringList=stringList[insertPoint:]
    newString="".join(newStringList)
    return newString

def getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray):
    string=getStringAtInsertPoint(mainList, lineNumber, insertPoint)
    stringRender=mainFont.render(string, True, textColor, backgroundColor)
    stringRect=getStringRect(stringRender, lineNumber, camerax, cameray)
    return stringRect

def getCursorRect(cursorX, cursorY, mainFont, camerax, cameray):
    cursor=mainFont.render('L', True, cursorColor)
    cursorRect=cursor.get_rect()
    cursorRect.x=cursorX-camerax
    cursorRect.y=cursorY-cameray
    return cursorRect

def setCursorToClick(mainList, cursorRect, mainFont, camerax, cameray, mouseX, mouseY):
    lineNumber=getLineNumberOfClick(mouseY, cameray, mainList)
    insertPoint=getInsertPointAtMouseX(mouseX, mouseY, lineNumber, mainList,
                                       mainFont, camerax, cameray)
    stringRect=getStringRectAtInsertPoint(mainList, lineNumber, insertPoint,
                                          mainFont, camerax, cameray)
    if(insertPoint==0):
        cursorRect.x=startX
    elif(insertPoint>0):
        cursorRect.x=stringRect.right
    cursorRect.y=stringRect.top
    return insertPoint, lineNumber, cursorRect

def getLineNumberOfClick(mouseY, cameray, mainList):
    clickLineNumber=(mouseY+cameray)/float(textHeight+(textHeight/4))
    if(clickLineNumber>len(mainList)):
        lineNumber=len(mainList)-1
    elif(clickLineNumber<=len(mainList)):
        floorLineNumber=math.floor(clickLineNumber)
        lineNumber=int(floorLineNumber)
    return lineNumber

def getInsertPointAtMouseX(mouseX, mouseY, lineNumber, mainList, mainFont, camerax, cameray):
    string=mainList[lineNumber]
    newInsertPoint = 0
    if((mouseY+cameray)>((lineNumber+1)*(textHeight+textHeight/4))):
        insertPoint=len(mainList[lineNumber])
        return insertPoint
    for insertPoint in string:
        stringRect=getStringRectAtInsertPoint(mainList, lineNumber, newInsertPoint
                                              , mainFont, camerax, cameray)
        if(mouseX>=stringRect.left):
            if(mouseX<stringRect.right):
                if(newInsertPoint>0):
                    return newInsertPoint-1
        newInsertPoint+=1
    else:
        return newInsertPoint

#having some bugs
inputDisplay=pygame.display.set_mode((inputDisplay_width, inputDisplay_height), RESIZABLE)
pygame.display.set_caption("Data")
icon=pygame.image.load("C:/Users/Downloads/data.png")
pygame.display.set_icon(icon)
inputDisplay.fill(backgroundColor)
notepad(inputDisplay)
pygame.display.update()
