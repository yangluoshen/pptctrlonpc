# -*- coding: cp936 -*-  
import Image  
import os, win32gui, win32ui, win32con, win32api  
   
def window_capture(dpath,imagetype = '.jpg'):  
    ''''' 
           @note:  截屏函数,调用方法window_capture('E:\\') ,参数为指定保存的目录 
                            返回图片文件名,文件名格式:ttt.jpg 
    '''  
    hwnd = 0  
    hwndDC = win32gui.GetWindowDC(hwnd)   
    mfcDC=win32ui.CreateDCFromHandle(hwndDC)   
    saveDC=mfcDC.CreateCompatibleDC()   
    saveBitMap = win32ui.CreateBitmap()   
    MoniterDev=win32api.EnumDisplayMonitors(None,None)  
    w = MoniterDev[0][2][2]  
    h = MoniterDev[0][2][3]  
    #print w,h　　　＃图片大小  
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)   
    saveDC.SelectObject(saveBitMap)   
    saveDC.BitBlt((0,0),(w, h) , mfcDC, (0,0), win32con.SRCCOPY)  
#     cc=time.gmtime()  
#     bmpname=str(cc[0])+str(cc[1])+str(cc[2])+str(cc[3]+8)+str(cc[4])+str(cc[5])+'.bmp'  
    bmpname = 'ttt'
    saveBitMap.SaveBitmapFile(saveDC, bmpname)  
    Image.open(bmpname).save(bmpname+imagetype)  
    os.remove(bmpname)  
    jpgname=bmpname+imagetype  
    djpgname=dpath+jpgname  
    copy_command = "move %s %s" % (jpgname, djpgname)  
    os.popen(copy_command)  
    return bmpname+imagetype  
   

def main():
    #调用截屏函数      
    window_capture('E:\\')  
    
if __name__ =="__main__":
    main()