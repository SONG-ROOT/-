#coding=utf-8
from PyQt5.QtWidgets import QMainWindow,QDesktopWidget,QLabel,QPushButton,QTextEdit,QFileDialog,QMessageBox
import os
from windows_api import UI

class CHOOSE_PWD(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 150, 800,500)
        self.center()
        self.main__UI()
        self.setWindowTitle('樱桃小丸子背单词     version 5.0 beta')    
        self.show()
    def center(self):             
        qr = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(center_point)
        self.move(qr.topLeft())

    def main__UI(self):#主UI
        lbl1=QLabel('优先从存档中读取单词,词库不足时,将会从你选择的单词本加载单词\n你可单击按钮选择文件所在路径',self);lbl1.setGeometry(10,10,800,100)
        btn1=QPushButton('单词本路径',self);btn1.setGeometry(10,110,100,30)
        self.QTextEdit_1 = QTextEdit(self);self.QTextEdit_1.setGeometry(220,110,500,80)
        btn2=QPushButton('进入\n新的页面',self);btn2.setGeometry(200,300,150,150)
        self.QTextEdit_1.setText(os.path.join(os.getcwd(),'单词本.txt'))
        btn1.clicked.connect(self.path_choose)
        btn2.clicked.connect(self.ks_ii_p)

    def path_choose(self):
        home=os.getcwd()
        fname = QFileDialog.getOpenFileName(self, 'Open file', home)
        if fname[0]:
            self.QTextEdit_1.setText(fname[0])
    def ks_ii_p(self):
        a=os.path.exists(self.QTextEdit_1.toPlainText())
        if a == 0:
            QMessageBox.warning(self, '？','文件不存在！，请重新选择')
            return 0
        self.hide()
        self.other_ui=UI.main(self.QTextEdit_1.toPlainText())