# coding:utf-8
import web
import os
import imagegrab
import sys

urls = (
        "/","index",
        "/(.*)","pic",
)
class index:
    def GET(self, name = None):
        web.header("Content-Type","text/html")
        return open("image/file.html","r").read()

class pic:
    def GET(self, name):
        print name
        path = os.getcwd()+'\\'+'image\\'
        imagegrab.window_capture(path,)
#         print path
        web.header("Content-Type", "image/jpeg")
        return open("image/ttt.jpg","rb").read()
app = web.application(urls,globals())
def close():
    app.stop()
def main(ip):
#     print web.ctx["ip"]
#     print"host is ",host
    sys.argv.append("%s:2015"%ip)
    app.run()
if __name__ == "__main__":
    app.run()
    