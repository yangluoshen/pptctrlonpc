#encoding=utf-8
'''
Created on 2014��5��22��

@author: yangluo
'''

import win32api
import win32con
from win32api import GetSystemMetrics
from ctypes import windll
from win32gui import GetCursorPos

screenMetrics = (GetSystemMetrics(0),GetSystemMetrics(1))

bottomOfScreen = screenMetrics

preDevicePos = [0,0]
# jumpButtonPos = (100,screenMetrics[1]-50)
# restartButtonPos = (150,screenMetrics[1]-50)
# fullscreenButtonPos = (300,screenMetrics[1]-50)
# escapeButtonPos = (200,screenMetrics[1]-50)
# startButtonPos = (250,screenMetrics[1]-50)


keymap = { 'fullscreen': 116,
           'last':       38,
           'next':       32,
           'escape':     27,
           }

def execute(keytype="move",key='next',keypos=bottomOfScreen):
    if keytype=="move":
        if preDevicePos[0]==0 and preDevicePos[1]==0:
            preDevicePos[0] = keypos[0]
            preDevicePos[1] = keypos[1]
            print "******************first************"
            return
        
        _newpos = [keypos[0]-preDevicePos[0],keypos[1]-preDevicePos[1]]
        print "_newpos is "+str(_newpos)
        currpos = GetCursorPos()
        newpos = myVector(currpos,_newpos)
        print 'new pos is ' + str(newpos)
        setCursorPos(newpos)
        preDevicePos[0] = keypos[0]
        preDevicePos[1] = keypos[1]
#         mouseclick(keypos)
    elif keytype=="commonkey":
        _key = keymap.get(key)
        if _key == None:
            return False
        keyboardevent(key)
    else:
        print "no this keytype: %s"%keytype
        return False
    
    return True
    

def mouseclick(targetCor):
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,targetCor[0],targetCor[1])
    win32api.Sleep(50)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,targetCor[0],targetCor[1])

def setCursorPos(mousepos):
    windll.user32.SetCursorPos(mousepos[0],mousepos[1])
    return True
    
def keyboardevent(key, delay=45):
    win32api.keybd_event(key,0,0,0)
    win32api.Sleep(delay)
    win32api.keybd_event(key,0,win32con.KEYEVENTF_KEYUP,0)
    
def myVector(currentPos, newPos):    
    resultPos = (currentPos[0]+newPos[0], currentPos[1]+newPos[1])
    return resultPos
def Istolong(newpos):
    sub = (newpos[0]-preDevicePos[0],newpos[1]-preDevicePos[1])
    if -3<sub[0]<3 and -3<sub[1]<3:
        return newpos
    _newpos = (newpos[0]+sub[0],newpos[1]+sub[1])
    return _newpos

