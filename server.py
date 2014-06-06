#coding:utf8
import socket
import keyevent
import os
# import threading

netIP = "127.0.0.1"
netPort1 = 2014
netPort2 = 2015
cursortype = {'ppt_normal_pen':     1,
              'ppt_laser_pen':      2,
              'ppt_huashua_pen':    3,
              'ppt_huabi_pen':      4,
              'ppt_xiangpica_pen':  5,
              }
class Server:

    def __init__(self):
        def on_close(sig):
            self.close()

        # win32api.SetConsoleCtrlHandler(on_close, True)
        print 'start ...'
        self.listening = True
        self.port = 2014
        self.ip = None
        self.server = None

    def getBindIp(self):
        s = socket.socket()
        s.bind(("127.0.0.1",self.port))
        self.ip = self.getIp()
        s.close()
        return self.ip
    def getIp(self):
        hostname = socket.gethostname()
        realIp = socket.gethostbyname(hostname)
        return realIp
        # 将主机名转换为IPv4地址, 但返回元组(hostname, aliaslist, ipaddrlist), 
        # 其中hostname是主机名, aliaslist是同一个地址的可选主机名列表, 
        # ipaddrlist是同一个主机上同一个接口的IPv4垃址列表。
        iplist = socket.gethostbyname_ex(hostname)[2]
        print iplist
        print realIp
        if len(iplist) == 0:
            return iplist[0]
        for ip in iplist:
            # print ip
            if ip[0:2] != '10':
                return ip
        return realIp

    def run(self):
        self.server = socket.socket()
#         print "selfip is ",self.ip
        self.server.bind((self.ip,self.port))
        # server.bind((ip,self.port))
        print 'listen at %s:%d' % (self.ip,self.port)
        self.server.listen(5)
        while self.listening:
            try:
                con,addr = self.server.accept()
                msg = con.recv(100)
#                 print addr,msg
                if msg == 'close':
                    self.listening = False
                type = msg.split(':')[0]
                if type == 'move':
                    pos = (int(float(msg.split(':')[1].split(',')[0])),int(float(msg.split(':')[1].split(',')[1])))
                    keyevent.execute(keytype=type, keypos=pos)
                elif type == 'mouse_up':
                    keyevent.execute(keytype=type)
                elif cursortype.get(msg) != None:
                    keyevent.choosePen(msg)
                else:
                    #if pppt_exit execute twice
                    if msg == 'ppt_exit':
                        keyevent.execute("commonkey",msg)
                    keyevent.execute("commonkey",msg)
#                 elif msg == 'ppt_full':
#                     keyevent.execute('commonkey', 'ppt_full')
#                 elif msg == 'ppt_exit':
#                     keyevent.execute("commonkey", "ppt_exit")
#                 elif msg == 'ppt_right':
#                     keyevent.execute("commonkey", "ppt_right")
#                 elif msg == 'ppt_left':
#                     keyevent.execute("commonkey", "ppt_left")
                
                con.close()
            except Exception as e:
                print e
    def httpServer(self):
        pass
    def close(self):
#         self.listening = False
        sock = socket.socket()
        sock.connect((self.ip,netPort1))
        sock.send("close")
        sock.close()
        self.server.close()

def webpyHandle():
#     os.system("python httpserver.py %s:2015"%netIP)
    pass
def main():
    try:
        s = Server()
#         global netIP
        netIP = s.getBindIp()
#         print netIP
        #start webpy server
#         Handle = threading.Thread(target=s.run)
#         Handle.start()
        s.run()
        
    except Exception as e:
        print e
#         raw_input()

if __name__ == "__main__":
    main()
