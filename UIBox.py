# -*- coding: cp936 -*-
# import pygame
import wx
import os
import win32com.client
# import keyevent
import server
import threading
import httpserver



window_size = (420,350)
button_size = (80,80)
filelist_size = (350,200)

frame_colour = wx.Colour(255,255,255)
text_colour = wx.Colour(40,139,213)

totalFileList = []
pptApplication = win32com.client.DispatchEx("PowerPoint.Application")


class MyFrame(wx.Frame):
    def __init__(self,image=None,parent=None,id=-1,pos=wx.DefaultPosition,title="PPTCtrl"):
        framestyle = wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER | 
                                        wx.RESIZE_BOX | wx.MAXIMIZE_BOX)
        wx.Frame.__init__(self,parent,id,title,pos,size=window_size,style=framestyle)
        self.Bind(wx.EVT_CLOSE,self.OnClose)
    def OnClose(self,event):
        print 'destroy'
        self.Destroy()
        
class MyApp(wx.App):
    def __init__(self,redirect=False):
        wx.App.__init__(self,redirect)
        self.pptlist = []
        self.netIP = None
        self.ppt_chosen = "None"
        self.sock = None
        self.socketHandle = threading.Thread(target=self.sockServer)
        self.socketHandle.start()
        self.webpyHandle = threading.Thread(target=self.webpyServer)
        self.webpyHandle.start()
    def OnExit(self):
        self.sock.close()
        httpserver.close()
    def OnInit(self):
        self.Font = wx.Font(15,wx.MODERN,wx.NORMAL,wx.NORMAL)
        
        self.win = MyFrame()
        bkg = wx.Panel(self.win)
        bkg.SetBackgroundColour(frame_colour)
        
#         browser_image = wx.Image("browserbtn.jpg",wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        boxlist = []
        hbox1 = wx.BoxSizer()
        boxlist.append(hbox1)
#         browser_size = (browser_image.GetWidth, browser_image.GetHight)
        self.browser_btn = wx.Button(bkg,label="browser")
        self.browser_btn.Bind(wx.EVT_BUTTON,self.Browser)
        self.start_btn = wx.Button(bkg,label="start")
        self.start_btn.Bind(wx.EVT_BUTTON,self.StartButton)
        boxlist[-1].Add(self.browser_btn,flag=wx.EXPAND)
        boxlist[-1].Add(self.start_btn,flag=wx.EXPAND)
        
        self.textPPTChosen = wx.StaticText(bkg,-1,label="Drag ppts here")
        self.textPPTChosen.SetFont(self.Font)
        self.fileList = wx.ListBox(bkg,style=wx.TE_MULTILINE|wx.HSCROLL,size=filelist_size)
        self.fileList.SetForegroundColour(text_colour)
        self.fileList.SetFont(self.Font)
        self.fileList.Bind(wx.EVT_LISTBOX, self.OnChoose)
        self.fileList.Bind(wx.EVT_LISTBOX_DCLICK,self.DClick)
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        boxlist.append(vbox)
        boxlist[-1].Add(self.textPPTChosen,flag=wx.EXPAND,border=5)
        boxlist[-1].Add(self.fileList,flag=wx.EXPAND,border=10)
        
        dropfile = MyFileDropTarget(self.fileList)
        self.fileList.SetDropTarget(dropfile)
        
        totalbox = wx.BoxSizer(wx.VERTICAL)
        for box in boxlist:
            totalbox.Add(box,flag=wx.EXPAND|wx.ALL,border=5)
        
        bkg.SetSizer(totalbox)
        self.win.Show()
        return True
 
    def Browser(self,event):
        file_wlidcard = "*.ppt;*.pptx"
        fdlg = wx.FileDialog(self.win,'choose pptfile',os.getcwd(),wildcard=file_wlidcard,style=wx.OPEN)
        
        if fdlg.ShowModal() == wx.ID_OK:
            sourceFileDir = fdlg.GetDirectory()
            filename = fdlg.GetFilename()
            self.ppt_chosen = sourceFileDir+'\\\\'+filename
            self.textPPTChosen.SetLabel(filename)
            totalFileList.append(self.ppt_chosen)
            item = [filename]
            self.fileList.InsertItems(item,0)
            fdlg.Destroy()
        else:
            return
    def sockServer(self):
        try:
            self.sock = server.Server()
            self.netIP = self.sock.getBindIp()
#             print 'sockserver self.netip',self.netIP

            self.sock.run()
            
        except Exception as e:
            print e
    def webpyServer(self):
        while self.netIP == None:
            pass
        netIP = self.sock.getBindIp()   
        httpserver.main(netIP) 
#         print 'webpy server ip is ',netIP
#         os.system("python httpserver.py %s:2015"%netIP)

            
    def OnChoose(self,event):
        self.textPPTChosen.SetLabel(event.GetString())
        self.ppt_chosen = totalFileList[len(totalFileList)-self.fileList.GetSelection()-1]
        
#         print "onChoose:%s"%event.GetString()
    def DClick(self,event):
        self.textPPTChosen.SetLabel(event.GetString())
#         print "DClick:"+totalFileList[event.GetSelection()]
        self.ppt_chosen = totalFileList[len(totalFileList)-self.fileList.GetSelection()-1]
        filepath = self.ppt_chosen
        self.startppt(filepath)
    def startppt(self,filepath):
        try:
            if os.path.isfile(filepath):
                filepath.replace('\\','\\\\')
                pptApplication.Presentations.Open(filepath)
                pptApplication.Visible = True
                pptApplication.WindowState = 1
        except Exception as e:
                print e
    def StartButton(self,event):
        filepath = self.ppt_chosen
        if not os.path.isfile(filepath):
            return False
        self.startppt(filepath)
        return True   
         
class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self,window):
        wx.FileDropTarget.__init__(self)
        self.window = window
    def OnDropFiles(self,x,y,filenames):
#         self.window.AppendText("")
        for file in filenames:
            ext = file.split('.')[-1]
            if ext=='ppt' or ext=='pptx' or ext=='pptm' \
                or ext=='PPT' or ext=='PPTX' or ext=='PPTM':
                item = [file.split('\\')[-1]]
                self.window.InsertItems(item,0)
                totalFileList.append(file)
            else:
                pass

def main():
    app = MyApp()
    app.MainLoop()
if __name__ == "__main__":
    main()


