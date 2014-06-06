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

currentpen = 1
press = False

keymap = { 'ppt_full':  116,
           'ppt_left':   38,
           'ppt_right':  40,
           'ppt_exit':   27,
           }
cursortype = {'ppt_normal_pen':     1,
              'ppt_laser_pen':      2,
              'ppt_huashua_pen':    3,
              'ppt_huabi_pen':      4,
              'ppt_xiangpica_pen':  5,
              }
# cursormap ={1:65}

def execute(keytype="move",key='ppt_right',keypos=bottomOfScreen):
    if keytype=="move":
#         print "left mouse click"
        if preDevicePos[0]==0 and preDevicePos[1]==0:
            pass
        else : 
            currpos = GetCursorPos()
            _newpos = [keypos[0]-preDevicePos[0],keypos[1]-preDevicePos[1]]
            if not Istolong(keypos):
                newpos = myVector(currpos,_newpos)
                setCursorPos(newpos)
                if press:
                    mouseclick(newpos)
        preDevicePos[0] = keypos[0]
        preDevicePos[1] = keypos[1]
    elif keytype=="mouse_up":
        pos = GetCursorPos()
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,pos[0],pos[1])
    elif keytype=="commonkey":
        _key = keymap.get(key)
        if _key == None:
            return False
        keyboardevent(_key)
    else:
        print "no this keytype: %s"%keytype
        return False
    
    return True
    

def mouseclick(targetCor):
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,targetCor[0],targetCor[1])
#     win32api.Sleep(50)
#     win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,targetCor[0],targetCor[1])

def setCursorPos(mousepos):
    windll.user32.SetCursorPos(mousepos[0],mousepos[1])
    return True
    
def keyboardevent(key, delay=5):
    win32api.keybd_event(key,0,0,0)
    win32api.Sleep(delay)
    win32api.keybd_event(key,0,win32con.KEYEVENTF_KEYUP,0)

def choosePen(pen='ppt_normal_pen'):
    _pen = cursortype.get(pen)
    if _pen == None:
        return None
    global currentpen
    global press
    if _pen == 1:
        press = False
        pos = GetCursorPos()
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,pos[0],pos[1])
        if currentpen != 1:
            currentpen = 1
            win32api.keybd_event(17,0,0,0)
            win32api.keybd_event(65,0,0,0)
#             win32api.Sleep(5)
            win32api.keybd_event(65,0,win32con.KEYEVENTF_KEYUP,0)
            win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)
    if _pen == 2:
        press = False
        pos = GetCursorPos()
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,pos[0],pos[1])
        if currentpen != 2:
            currentpen = 2
            win32api.keybd_event(17,0,0,0)
            win32api.keybd_event(76,0,0,0)
#             win32api.Sleep(5)
            win32api.keybd_event(76,0,win32con.KEYEVENTF_KEYUP,0)
            win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)
    if _pen == 3:
        press = True
        pos = GetCursorPos()
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,pos[0],pos[1])
        if currentpen != 3:
            currentpen = 3
            win32api.keybd_event(17,0,0,0)
            win32api.keybd_event(73,0,0,0)
#             win32api.Sleep(5)
            win32api.keybd_event(73,0,win32con.KEYEVENTF_KEYUP,0)
            win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)
    if _pen == 4:
        press = True
        pos = GetCursorPos()
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,pos[0],pos[1])
        if currentpen != 4:
            currentpen = 4
            win32api.keybd_event(17,0,0,0)
            win32api.keybd_event(80,0,0,0)
#             win32api.Sleep(5)
            win32api.keybd_event(80,0,win32con.KEYEVENTF_KEYUP,0)
            win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)
    if _pen == 5:
        press = True
        pos = GetCursorPos()
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,pos[0],pos[1])
        if currentpen != 5:
            currentpen = 5
#             win32api.keybd_event(17,0,0,0)
            win32api.keybd_event(69,0,0,0)
#             win32api.Sleep(5)
            win32api.keybd_event(69,0,win32con.KEYEVENTF_KEYUP,0)
#             win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)
    
def myVector(currentPos, subPos):    
    resultPos = (currentPos[0]+subPos[0], currentPos[1]+subPos[1])
    return resultPos
def Istolong(newpos):
    '''
    @note: you can adjust the value of 'subBoundry' to adjust the move speed 
            of the cursor
    '''
    sub = (newpos[0]-preDevicePos[0],newpos[1]-preDevicePos[1])
    subBoundry = 50
    if -subBoundry<sub[0]<subBoundry and -subBoundry<sub[1]<subBoundry:
        return False
    return True

