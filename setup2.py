#encoding:utf-8
#!python
# -*- coding: gb2312 -*-
 
# �芒赂枚陆�卤戮�篓�陋pygame��禄炉拢卢�鹿��py2exe麓貌掳眉麓煤�毛潞����麓��dist�驴�录
#
# �鹿�����么�����芒拢卢驴����么����拢潞
#  http://eyehere.net/2011/python-pygame-novice-professional-py2exe/
#
# 掳虏�掳�猫�贸:
#         python, pygame, py2exe 露录�娄赂��掳��
 
# �鹿��路陆路篓:
#         1: ��赂�麓���录镁拢卢�赂露篓�猫�陋麓貌掳眉碌�.py潞�露��娄�媒戮�
#         2: python pygame2exe.py
#         3: ��dist��录镁录���拢卢enjoy it~
 
try:
    from distutils.core import setup
    import py2exe, pygame
    from modulefinder import Module
    import glob, fnmatch
    import sys, os, shutil
except ImportError, message:
    raise SystemExit,  "Sorry, you must install py2exe, pygame. %s" % message
 
# �芒赂枚潞炉�媒�����麓��露�DLL��路帽���碌�鲁�谩鹿漏碌�拢篓��碌�禄掳戮�虏禄��麓貌掳眉拢漏
origIsSystemDLL = py2exe.build_exe.isSystemDLL
def isSystemDLL(pathname):
    # �猫�陋hack�禄��拢卢freetype潞�ogg碌�dll虏垄虏禄���碌�鲁DLL
    if os.path.basename(pathname).lower() in ("libfreetype-6.dll", "libogg-0.dll", "sdl_ttf.dll"):
        return 0
    return origIsSystemDLL(pathname)
# 掳�Hack鹿媒碌�潞炉�媒�����麓禄��楼
py2exe.build_exe.isSystemDLL = isSystemDLL
 
# �芒赂枚��碌����虏���禄赂枚Hack拢卢�鹿碌�pygame碌��卢�����氓禄谩卤禄驴陆卤麓
class pygame2exe(py2exe.build_exe.py2exe):
    def copy_extensions(self, extensions):
        # 禄帽碌�pygame�卢�����氓
        pygamedir = os.path.split(pygame.base.__file__)[0]
        pygame_default_font = os.path.join(pygamedir, pygame.font.get_default_font())
        # 录��毛驴陆卤麓��录镁��卤铆
        extensions.append(Module("pygame.font", pygame_default_font))
        py2exe.build_exe.py2exe.copy_extensions(self, extensions)
 
# �芒赂枚���������忙�媒�枚���茅碌�虏驴路�
class BuildExe:
    def __init__(self):
        #------------------------------------------------------#
        ##### 露����禄赂枚��碌����路鲁��貌拢卢�猫�陋��赂��芒�茂碌�赂梅赂枚虏��媒 #####
        #--------------------------------------------------- ---#
 
        # �冒�录py��录镁
        self.script = "UIBox.py"
        # ���路�没
        self.project_name = "pptbird"
        # ���路site
        self.project_url = "about:none"
        # ���路掳忙卤戮
        self.project_version = "0.0"
        # ���路�铆驴�
        self.license = "bubble License"
        # ���路�梅��
        self.author_name = "yangluo"
        # �陋�碌碌莽��
        self.author_email = "649673800@qq.com"
        # ���路掳忙�篓
        self.copyright = "Copyright (c) yangluo."
        # ���路�猫�枚
        self.project_description = "testsocket Description"
        # ���路�录卤锚(None碌�禄掳�鹿��pygame碌��卢���录卤锚)
        self.icon_file = None
        # 露卯�芒�猫�陋驴陆卤麓碌���录镁隆垄��录镁录�(�录�卢拢卢�么�碌碌�)
        self.extra_datas = ["image"]
        # 露卯�芒�猫�陋碌�python驴芒�没
        self.extra_modules = []
        # �猫�陋��鲁媒碌�python驴芒
        self.exclude_modules = []
        # 露卯�芒�猫�陋��鲁媒碌�dll
        self.exclude_dll = ['']
        # �猫�陋录��毛碌�py��录镁
        self.extra_scripts = []
        # 麓貌掳眉Zip��录镁�没(None碌�禄掳拢卢麓貌掳眉碌陆exe��录镁��)
        self.zipfile_name = None
        # �煤鲁���录镁录�
        self.dist_dir ='pptctrldir'
 
    def opj(self, *args):
        path = os.path.join(*args)
        return os.path.normpath(path)
 
    def find_data_files(self, srcdir, *wildcards, **kw):
        # 麓��麓��录镁录���禄帽�隆��录镁
        def walk_helper(arg, dirname, files):
            # 碌卤�禄�茫�鹿���盲�没碌�掳忙卤戮驴���鹿陇戮��虏�麓碌�拢卢�虏驴���录�陆酶�麓
            if '.svn' in dirname:
                return
            names = []
            lst, wildcards = arg
            for wc in wildcards:
                wc_name = self.opj(dirname, wc)
                for f in files:
                    filename = self.opj(dirname, f)
 
                    if fnmatch.fnmatch(filename, wc_name) and not os.path.isdir(filename):
                        names.append(filename)
            if names:
                lst.append( (dirname, names ) )
 
        file_list = []
        recursive = kw.get('recursive', True)
        if recursive:
            os.path.walk(srcdir, walk_helper, (file_list, wildcards))
        else:
            walk_helper((file_list, wildcards),
                        srcdir,
                        [os.path.basename(f) for f in glob.glob(self.opj(srcdir, '*'))])
        return file_list
 
    def run(self):
        if os.path.isdir(self.dist_dir): # �戮鲁媒��麓�碌��煤鲁�陆谩鹿没
            shutil.rmtree(self.dist_dir)
 
        # 禄帽碌��卢���录卤锚
        if self.icon_file == None:
            path = os.path.split(pygame.__file__)[0]
            self.icon_file = os.path.join(os.getcwd(), 'image/logo.ico')
 
        # 禄帽碌��猫�陋麓貌掳眉碌��媒戮���录镁
        extra_datas = []
        for data in self.extra_datas:
            if os.path.isdir(data):
                extra_datas.extend(self.find_data_files(data, '*'))
            else:
                extra_datas.append(('.', [data]))
 
        # 驴陋�录麓貌掳眉exe
        setup(
            cmdclass = {'py2exe': pygame2exe},
            version = self.project_version,
            description = self.project_description,
            name = self.project_name,
            url = self.project_url,
            author = self.author_name,
            author_email = self.author_email,
            license = self.license,
 
            # �卢���煤鲁�麓掳驴�鲁��貌拢卢�莽鹿没�猫�陋�煤鲁���露�鲁��貌(debug陆�露�)拢卢�鹿��拢潞
            # console = [{
            windows = [{
                'script': self.script,
                'icon_resources': [(0, self.icon_file)],
                'copyright': self.copyright
            }],
            options = {'py2exe': {'optimize': 2, 'bundle_files': 1,
                                  'compressed': True,
                                  'excludes': self.exclude_modules,
                                  'packages': self.extra_modules,
                                  'dist_dir': self.dist_dir,
                                  'dll_excludes': self.exclude_dll,
                                  'includes': self.extra_scripts} },
            zipfile = self.zipfile_name,
            data_files = extra_datas,
            )
 
        if os.path.isdir('build'): # �氓鲁媒build��录镁录�
            shutil.rmtree('build')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.argv.append('py2exe')
    BuildExe().run() 
    raw_input("Finished! Press any key to exit.")