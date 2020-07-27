#coding=utf-8
import sys,os,ctypes
if hasattr(sys, 'frozen'):
   os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5.QtWidgets import QApplication
from windows_api import First_choose

if os.name=='nt':
    whnd1 = ctypes.windll.kernel32.GetConsoleWindow()
    ctypes.windll.user32.ShowWindow(whnd1, 0)
    ctypes.windll.kernel32.CloseHandle(whnd1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = First_choose.CHOOSE_PWD()
    sys.exit(app.exec_())