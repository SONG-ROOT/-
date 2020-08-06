#coding=utf-8
from PyQt5.QtWidgets import QMainWindow,QDesktopWidget,QLineEdit,QTextEdit,\
    QPushButton,QAction,QMessageBox,QFontDialog,QColorDialog,QFileDialog,QLabel
from PyQt5.QtGui import QIcon
import os,random,requests,re,json,webbrowser
from lxml import etree
from PyQt5.QtCore import Qt

class main(QMainWindow):

    def __init__(self,path_you_choose):
        with open('data/请求头.txt','r',encoding='utf-8') as f:
            self.User_Agent=f.readlines()[0].replace('\n','')
        self.word_book_path=path_you_choose

        self.list_main=[]#正在背的单词库
        self.list_temporary1=[]#临时词库
        self.list_temporary2=[]#已背的单词库

        self.list5=''#查重复的路径
        self.CTRL=0#快速查词或直接翻译
        self.count=0#已背单词计数

        super().__init__()
        self.initUI()
        

    def initUI(self):
        self.setGeometry(200, 150, 1800,900)
        self.center()#窗口布置在中心
        self.main__UI()
        self.setWindowTitle('樱桃小丸子背单词     version 5.0 beta')    
        self.setWindowIcon(QIcon(r'data\1.ico'))
        self.show()
    def center(self):             
        qr = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(center_point)
        self.move(qr.topLeft())

#############################    UI    ############################################
    def main__UI(self):#主UI
        #英文单词框
        self.text__danci = QLineEdit(self);self.text__danci .setGeometry(20,50,875,250);self.text__danci.setReadOnly(True)
        self.text__fanyi = QTextEdit(self);self.text__fanyi .setGeometry(20,350,875,400)#中文翻译框
        self.text__juzi = QTextEdit(self);self.text__juzi .setGeometry(905,50,875,600)#例句框
        self.YOU_WANT = QTextEdit(self);self.YOU_WANT .setGeometry(905,720,400,50)#快速查词框
        #经验数量
        self.DUAN_WEI_EXP = QTextEdit(self);self.DUAN_WEI_EXP .setGeometry(990,770,350,40);self.DUAN_WEI_EXP.setTextInteractionFlags(Qt.NoTextInteraction)
        #发音
        self.english__tip = QTextEdit(self);self.english__tip .setGeometry(230,300,500,40);self.english__tip.setReadOnly(True)

        #OK,no按钮
        self.btnok=QPushButton('单词我认识了\n，下一个吧  (P)',self);self.btnok.setToolTip('点击后开始下一个单词，且此单词以后不再抽到');self.btnok.setGeometry(1580,760,200,100)
        self.btnno=QPushButton('至少一个单词不会，\nso下次还会抽到  (X)',self);self.btnno.setToolTip('点击后开始下一个单词，且此单词下次还会抽到');self.btnno.setGeometry(1360,760,200,100)
        #所有的都翻译
        self.btnall=QPushButton('单词一键翻译\n(懒人必备)  (Z)',self);self.btnall.setGeometry(400,760,200,100)
        #说明按钮
        btn1=QPushButton('英式发音与美式发音',self);btn1.setGeometry(20,300,200,40)
        btn5=QPushButton('翻译框',self);btn5.setGeometry(20,760,100,40)
        self.btn__shoucang=QPushButton('收藏单词 ()',self);self.btn__shoucang.setGeometry(150,760,150,40)
        self.btn__YOU_WANT=QPushButton('快速查词',self);self.btn__YOU_WANT.setGeometry(905,660,100,50)
        self.DUAN_WEI=QLabel('临时统计',self);self.DUAN_WEI.setGeometry(905,770,80,30)

        #btn6=QPushButton('手动发音',self);btn6.setGeometry(1680,300,80,30);btn7=QPushButton('手动发音',self);btn7.setGeometry(780,300,80,30)
        btnoo=QPushButton('例句',self);btnoo.setGeometry(1700,650,80,30)

        exitAction = QAction(QIcon(r'data\1.ico'), '&字体', self);exitAction.setShortcut('Ctrl+Q');exitAction.setStatusTip('哦吼换种字体吧')
        exitAction1 = QAction(QIcon(r'data\1.ico'), '框的颜色', self);exitAction1.setShortcut('Ctrl+W');exitAction1.setStatusTip('可以换颜色哦')
        exitAction2 = QAction(QIcon('data\2.ico'), '单词本查重复', self);exitAction2.setStatusTip('点击后将查出重复单词，并展示')
        exitAction3 = QAction(QIcon('data\3.ico'), '单词本一键去重复', self);exitAction3.setStatusTip('直接去除重复，但不会列出重复单词')
        exitAction4 = QAction(QIcon('data\4.ico'), '快速翻译', self);exitAction4.setShortcut('Z');exitAction4.setStatusTip('贼jb懒');exitAction5 = QAction(QIcon('data\5.ico'), '返回', self)
        exitAction6 = QAction(QIcon('data\6.ico'), '会 下一组单词', self);exitAction6.setShortcut('P')
        exitAction7 = QAction(QIcon('data\7.ico'), '不会 下一组单词', self);exitAction7.setShortcut('X')
        exitAction8 = QAction(QIcon('data\8.ico'), '用户使用须知', self);exitAction8.setShortcut('Ctrl+S')
        
        exitAction9 = QAction(QIcon('data\8.ico'), '单词单独控制字体', self)
        exitAction10 = QAction(QIcon('data\8.ico'), '单词单独控制颜色', self)
        exitAction11= QAction(QIcon('data\8.ico'), '翻译单独控制字体', self)
        exitAction12 = QAction(QIcon('data\8.ico'), '翻译单独控制颜色', self)
        exitAction13 = QAction(QIcon('data\8.ico'), '例句单独控制字体', self)
        exitAction14 = QAction(QIcon('data\8.ico'), '例句单独控制颜色', self)
        exitAction15 = QAction(QIcon('data\8.ico'), 'python', self)
        exitAction666=QAction(QIcon('data\1.ico'), '访问金山词霸', self)
        exitAction33=QAction(QIcon('data\1.ico'), '修改浏览器请求头', self);exitAction33.setStatusTip('别问浏览器和本程序有什么关系，问就是本程序伪装成浏览器')
        exitAction_save=QAction(QIcon('data\1.ico'), '我要提前保存', self);exitAction_save.setStatusTip('定时保存，养成良好的使用习惯。防止程序crash时，丢失从单词本中加载的单词')


        self.statusBar()#创建一个菜单栏
        fileMenu =self.menuBar().addMenu('&总控制台')#菜单栏中添加主项
        fileMenu1 =self.menuBar().addMenu('&快捷键')
        fileMenu2 =self.menuBar().addMenu('&分控制台')
        fileMenu3 =self.menuBar().addMenu('&支持金山词霸！！')
        fileMenu4 =self.menuBar().addMenu('&支持金山词霸！！')
        fileMenu5 =self.menuBar().addMenu('&保存记录，以免程序崩溃时丢失单词！！')
        fileMenu6 =self.menuBar().addMenu('&封锁访问？')
        #添加写好的exitAction事件
        fileMenu.addAction(exitAction);fileMenu.addAction(exitAction1);fileMenu.addAction(exitAction2);fileMenu.addAction(exitAction3);fileMenu.addAction(exitAction15);fileMenu.addAction(exitAction5)
        fileMenu1.addAction(exitAction4);fileMenu1.addAction(exitAction6);fileMenu1.addAction(exitAction7);fileMenu1.addAction(exitAction8)
        fileMenu2.addAction(exitAction9);fileMenu2.addAction(exitAction10);fileMenu2.addAction(exitAction11);fileMenu2.addAction(exitAction12);fileMenu2.addAction(exitAction13);fileMenu2.addAction(exitAction14)
        fileMenu6.addAction(exitAction33)
        fileMenu3.addAction(exitAction666)
        fileMenu5.addAction(exitAction_save)
        
        exitAction7.triggered.connect(self.buttonClicked__1);exitAction6.triggered.connect(self.buttonClicked__2);exitAction4.triggered.connect(self.translate__my)

        exitAction.triggered.connect(self.MY__QFontDialog);exitAction1.triggered.connect(self.MY__QColorDialog)
        exitAction2.triggered.connect(self.FIND);exitAction3.triggered.connect(self.delete__word);exitAction8.triggered.connect(self.tellabout)
        exitAction9.triggered.connect(self.slect__chuanru);exitAction10.triggered.connect(self.slect__chuanru);exitAction11.triggered.connect(self.slect__chuanru);exitAction12.triggered.connect(self.slect__chuanru);exitAction13.triggered.connect(self.slect__chuanru);exitAction14.triggered.connect(self.slect__chuanru)
        exitAction15.triggered.connect(self.fly);exitAction666.triggered.connect(self.fly1);exitAction33.triggered.connect(self.OPEN_AGENT)
        exitAction_save.triggered.connect(self.save_do)

        self.initialize_first()
        self.UI_event()
############################    UI_EVENT  LINK    #################################
    def UI_event(self):
        self.btnno.clicked.connect(self.buttonClicked__1)
        self.btnok.clicked.connect(self.buttonClicked__2)
        self.btnall.clicked.connect(self.translate__my)
        self.btn__shoucang.clicked.connect(self.shoucang)
        self.btn__YOU_WANT.clicked.connect(self.SINGLE_CHECK)
############################    单词处理    #################################
    def initialize_first(self): #程序初始化
        try:
            with open(os.getcwd()+r"\temporary\正在背的.txt",'r',encoding='utf-8') as A99:
                A100=A99.readlines()[0:]#加入新单词
            if len(A100) > 8:
                self.open__doing__file()
            elif len(A100) <= 8:
                QMessageBox.question(self, '提示！',"初始化提示：词库单词数小于等于八，准备加载新的一组单词", QMessageBox.Yes)
                self.open__doing__file()
                self.open__new__file()
        except Exception as e:
            print(str(e),'    ,UI.py : 1.初始化错误！可能是误删了正在背的.txt！')
        self.show__words()#不管大于八还是小于八，都展示单词

    def open__doing__file(self):#仅打开doing文档，把所有单词加入list_main
        try:
            with open(os.getcwd()+r"\temporary\正在背的.txt",'r',encoding='utf-8') as A1:
                A3=A1.readlines()[0:88]
            for i in A3:
                self.list_main.append(i)
                #print(self.list_main)
        except Exception as e:
            print(str(e),r'    ,UI.py : 2.初始化错误！可能是误删了 正在背的.txt')
    def open__new__file(self):#打开单词本,选出一些单词加入list_main,并把选出的单词从单词本中删掉(可以考虑增加限制)
        try:
            with open(self.word_book_path,'r',encoding='utf-8') as A:
                A2=A.readlines()[0:88]
            for i in A2:#必须添加，直接相等的话会把原先的删掉
                self.list_main.append(i)
            with open(self.word_book_path,'r',encoding='utf-8') as A4:
                A5=A4.readlines()[0:]
            rewrite1=set(A5)-set(A2)
            with open(self.word_book_path,'w',encoding='utf-8') as B1:
                for ii in rewrite1:
                    B1.write(ii)
        except Exception as e:
            print(str(e),r'    ,UI.py : 3.初始化错误！')
    def show__words(self):#仅从list__main中拿单词,保存到list_temporary1，在文字框中展示单词,调用前需要确保单词大于八
        try:
            if len(self.list_main) > 8:
                for i in range(1):#抽取1个,保存在list_temporary1中
                    self.list_temporary1.append(random.choice(self.list_main))
                self.text__danci .setText(self.list_temporary1[0])#记得每次这个列表初始化
            else:#单词不足八个时也会抽取
                self.list_temporary1.append(random.choice(self.list_main))
                self.text__danci .setText(self.list_temporary1[0])#记得每次这个列表初始化
        except Exception as e:
            print(str(e),'    ,UI.py : 4.未知错误！')
    def can__write__words(self):#会的单词从list_main删除，移入list_temporary2中记录
        try:
            for ir in self.list_temporary1:
                self.list_temporary2.append(ir)
                self.list_main.remove(ir)
                self.count=self.count+1
                self.count_it()
        except Exception as e:
            print(str(e),'    ,UI.py : 5.未知错误！')
    def save__q(self):#打开并格式化doing文档，把没背的list__main单词加入doing
        #打开beiwande的文档，list_temporary2追加写入到beiwande,这个文档只追加写入
        with open(os.getcwd()+r"\temporary\正在背的.txt",'w',encoding='utf-8') as A3:
            for it in self.list_main:
                A3.write(it)

        with open(os.getcwd()+r"\temporary\背完的.txt",'a',encoding='utf-8') as A8:
            for it in self.list_temporary2:
                A8.write(it)
############################    UI_EVENT    #################################
    def buttonClicked__1(self):#点不会按钮
        self.list_temporary1=[] 
        self.text__fanyi.setText("");self.english__tip.setText("");self.text__juzi.setText("")
        if len(self.list_main)==8:#小于八强制加单词
            QMessageBox.question(self, '提示！',"词库单词数等于八，准备加载新的一组单词", QMessageBox.Yes)
            self.open__new__file()
        elif len(self.list_main)<=1:
            QMessageBox.question(self, '提示！',"词库单词数小于等于1,且词库已经没有单词可添加！", QMessageBox.Yes)
            self.text__danci .setText("Compelete all the word!")
        elif len(self.list_main)<8:
            QMessageBox.question(self, '提示！',"词库单词数等于7,且词库已经没有单词可添加！但是剩余的八个单词将会继续抽", QMessageBox.Yes)
        self.show__words()#大于八直接抽单词

    def buttonClicked__2(self):#点会按钮
        self.text__fanyi.setText("");self.english__tip.setText("");self.text__juzi.setText("")
        if len(self.list_main)==8:#小于八强制加单词
            QMessageBox.question(self, '提示！',"词库单词数等于八，准备加载新的一组单词", QMessageBox.Yes)
            self.open__new__file()
        elif len(self.list_main)<=1:
            QMessageBox.question(self, '提示！',"词库单词数小于等于1,且词库已经没有单词可添加！", QMessageBox.Yes)
            self.text__danci .setText("Compelete all the word!")
        elif len(self.list_main)<8:
            QMessageBox.question(self, '提示！',"词库单词数小于等于7,且词库已经没有单词可添加！但是剩余的八个单词将会继续抽", QMessageBox.Yes)
        self.can__write__words() 
        self.list_temporary1=[] 
        self.show__words()#大于八直接抽单词

    def closeEvent(self, event):#退出询问
        reply=QMessageBox.question(self, 'Message',
            "保存并退出？？", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)  #弹出窗口的title名,字符串消息对话框中显示的文本,指定按钮的2个组合出现在对话框中，最后一个参数是默认按钮，和按钮焦点
        if reply == QMessageBox.Yes:#点击yes退出窗口
            event.accept()
            self.save__q()#存档
        else:
            event.ignore()
   
    def translate__my(self):#Core item
        header={
        "User-Agent":self.User_Agent
        }
        t__url="http://www.iciba.com/word?w="
        try:
            #key= str.strip("set")#测试
            if self.CTRL==0:#单词翻译
                key= str.strip(self.list_temporary1[0])
            elif self.CTRL==1:#快速查词
                key= str.strip(self.YOU_WANT.toPlainText())

            url=t__url+key
            response=requests.get(url,headers=header).text
            html=etree.HTML(response)
            #[\s\S]*?          (.*?)

            ###########################   仅翻译   #################################
            a=re.compile(r'<ul class="Mean_part__1RA2V">(.*?)</ul>').findall(response)
            result__base__translate=a[0].replace('<li>','').replace('</li>','').replace('<i>','\n').replace('</i>',' ').replace('<span>','').replace('</span>','').replace('<div>','').replace('</div>','').replace('<!-- -->','')
            self.text__fanyi.setText(result__base__translate)#显示翻译
            ########################### 单词与翻译 #####################################
            JSON_INIT=html.xpath(r'//script[@id="__NEXT_DATA__"]')
            JSON_CLEAN=JSON_INIT[0].text
            JS=json.loads(JSON_CLEAN)
            
            SETENSE_MEAN=JS['props']['initialDvaState']['word']['wordInfo']['new_sentence'][0]['sentences']
            #print(SETENSE_MEAN[0])
            REAL_CHINESE_AND_ENGLISH_MEAN=''
            for i in range(len(SETENSE_MEAN)):
                REAL_CHINESE_AND_ENGLISH_MEAN=REAL_CHINESE_AND_ENGLISH_MEAN+SETENSE_MEAN[i]['en']+'\n'+SETENSE_MEAN[i]['cn']+'\n'+SETENSE_MEAN[i]['from']+'\n\n'
            self.text__juzi.setText(REAL_CHINESE_AND_ENGLISH_MEAN)

            FAYIN=JS['props']['initialDvaState']['word']['wordInfo']['baesInfo']

            #print('\n',FAYIN,'\n')
            fayin_all= '英音: '+FAYIN['symbols'][0]['ph_en']+'  ,美音: '+FAYIN['symbols'][0]['ph_am']
            self.english__tip.setText(fayin_all)#显示发音
            
        except Exception as e:#捕获try语句里面的异常的对象
            print("错误 <总> ； ",e)

############################    美化多余功能    #################################
    def MY__QFontDialog(self): #字体                 
        font, ok = QFontDialog.getFont()#这一行代码弹出字体选择对话框，getFont()方法返回字体名称和ok参数，如果用户点击了ok他就是True,否则就是false
        if ok:
            self.text__danci.setFont(font)
            self.text__fanyi.setFont(font)
            self.text__juzi.setFont(font)
    def MY__QColorDialog(self):          
        col = QColorDialog.getColor()#这一行代码弹出QColorDialog
        if col.isValid():#Valid:有效的
            self.text__danci.setStyleSheet("QWidget { background-color: %s }"
                % col.name())
            self.text__fanyi.setStyleSheet("QWidget { background-color: %s }"
                % col.name())
            self.english__tip.setStyleSheet("QWidget { background-color: %s }"
                % col.name())
            self.text__juzi.setStyleSheet("QWidget { background-color: %s }"
                % col.name())
    def FIND(self):#单词重复检测
        list5=[]
        home=os.getcwd()
        fname = QFileDialog.getOpenFileName(self, '选择要扫描的单词本！', home)
        self.list5=fname[0]

        if fname[0]:
            pass
        else:
            QMessageBox.warning(self, '？','没有选择文件！')
            return '傻X'

        with open(fname[0],'r',encoding='utf-8') as W1:
            list4=W1.readlines()
        if(len( set(list4) ) == len(list4) ):
            print("无重复单词")
            reply=QMessageBox.question(self, '无重复',
                "提示：找不到重复单词？\n写的不规范将影响查找单词，如"+"1,"+"1 ,"+"1    ,"+"是不重复的", QMessageBox.Yes)
        else:
            for i in set(list4):
                if list4.count(i)>=2:
                    list5.append(i)

            reply=QMessageBox.question(self, '重复是',
                '\n\n出现了'+str(len(list5))+'\n个不同的重复单词，以上单词每个至少重复一次'+str(list5), QMessageBox.Yes)
    def delete__word(self):#单词本去重复
        if self.list5=='':
            QMessageBox.question(self, '没有设置目录?',"请先查找重复单词", QMessageBox.Yes)
            return 0
        reply=QMessageBox.question(self, '直接去重复你确定?',"重复单词将全部从  "+str(self.list5)+"  中删除？", QMessageBox.Yes| QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            with open(self.list5,'r',encoding='utf-8') as AQ:
                Aq=AQ.readlines()

            with open(self.list5,'w',encoding='utf-8') as dele:
                try:
                    for r in set(Aq):
                        dele.write(r)
                except Exception as e:
                    print(str(e),'    ,UI.py : 6.未知错误！')
        else:
            pass
    def tellabout(self):
        reply=QMessageBox.about(self, "用户使用须知",
            '大家好，我是渣渣灰，是兄弟就砍我，一刀九九九，装备全靠爆。下面是我要说的话:\n\
        0.快捷方式按一下就好，千万不要长按\
        1.请不要随意修改或删除程序下的文件夹及从任务管理器强制关闭程序，以免丢失单词\n 2.程序按行读取  你选择的单词本 的内容，必要时可以自己随意添加或删除单词本内容，每行可添加一个单词\
        3.使用翻译时必须联网,且翻译为此单词的全部意思,不分四级六级八级.分也可以但有些单词的某个意思四级考，另一个意思只有六级才考.所以意思会不全。我懒得处理\
        4.点击我已经认识这些单词了， 表示我已经学会这个单词了，且这单词以后不再抽到，退出时保存到 \ temporary\ 背完的.txt"中，也可手动保存\
        \n5.首次运行时，预加载 你选择的单词本 的 88个单词到内存中(同时立即从原有的单词本中删除这88个单词,所以要经常手动保存。以免程序崩溃时，丢失加载到内存中的单词),每内存词库不足8个时自动加载 你选择的单词本 的88个单词(并立即从单词本删除加载的部分),这8个单词将和下一组一起出现。退出时将自动保存未完成的部分到\ temporary\正在背的.txt下，下次优先从\ temporary\正在背的.txt加载单词\
        6.本可以爬取语音的但为了不给金山翻译服务器增加额外负担,就算了,自己看英式和美式英标脑补发音\
        8.退出时自动保存进度,也可手动保存\
        9.点击下一组，则下次还会再抽到这个单词\n谢谢！！\n                                             --荒野79' )
    def shoucang(self):
        with open(os.getcwd()+r"\temporary\收藏.txt",'a',encoding='utf-8') as s:
            s.write(self.text__danci.text())
        QMessageBox.question(self, '提示！',r"已经收藏了单词！目录：\ temporary \ 收藏.txt", QMessageBox.Yes)
    def slect__chuanru(self):
        sender = self.sender()
        def begin(a,b):
            if a==0 and b==0:
                font, ok = QFontDialog.getFont()
                if ok:
                    self.text__danci.setFont(font)
            if a==0 and b==1:
                col = QColorDialog.getColor()#这一行代码弹出QColorDialog
                if col.isValid():#Valid:有效的
                    self.text__danci.setStyleSheet("QWidget { background-color: %s }"
                        % col.name())
            if a==1 and b==0:
                font, ok = QFontDialog.getFont()
                if ok:
                    self.text__fanyi.setFont(font)
            if a==1 and b==1:
                col = QColorDialog.getColor()#这一行代码弹出QColorDialog
                if col.isValid():#Valid:有效的
                    self.text__fanyi.setStyleSheet("QWidget { background-color: %s }"
                        % col.name())
            if a==2 and b==0:
                font, ok = QFontDialog.getFont()
                if ok:
                    self.text__juzi.setFont(font)
            if a==2 and b==1:
                col = QColorDialog.getColor()#这一行代码弹出QColorDialog
                if col.isValid():#Valid:有效的
                    self.text__juzi.setStyleSheet("QWidget { background-color: %s }"
                        % col.name())
        if sender.text()=="单词单独控制字体":
            begin(0,0)
        elif sender.text()=="单词单独控制颜色":
            begin(0,1)
        elif sender.text()=="翻译单独控制字体":
            begin(1,0)
        elif sender.text()=="翻译单独控制颜色":
            begin(1,1)
        elif sender.text()=="例句单独控制字体":
            begin(2,0)
        elif sender.text()=="例句单独控制颜色":
            begin(2,1)
    def fly(self):
        #webbrowser.open("https://xkcd.com/353/")
        webbrowser.open("baike.baidu.com/item/python")
    def fly1(self):
        webbrowser.open("http://www.iciba.com/")
    def OPEN_AGENT(self):
        os.system('notepad.exe data/请求头.txt')
    def SINGLE_CHECK(self):
        self.CTRL=1
        self.translate__my()
        self.CTRL=0
    def save_do(self):#手动保存
       QMessageBox.information(self, '信息',"保存成功", QMessageBox.Yes)
       self.save__q()
    
    def count_it(self):
        self.DUAN_WEI_EXP.setText('自本次打开程序，已背会了'+str(self.count)+'个单词')