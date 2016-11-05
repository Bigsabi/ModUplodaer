# -*- coding:utf-8 -*-
import sys
from PyQt4 import QtCore,QtGui
from PyQt4.QtCore import Qt
import Updater
import Mod
import Helper
import os
import json
import urllib
import urllib2
import crifanLib
#全局变量
global ServerMods
ServerMods = []
global LocalMods
LocalMods = []
global mapp
global mw
__version__ = "0.1"
#更新部分
def U():
    State = mw.findChild(QtGui.QLabel,'State')
    NeedDeleteMods = []
    NeedDownloadMods = []
    #判断哪些Mod需要删除
    for Mod in ServerMods:
        if Mod.Delete is True:
            #判断是否在本地存在 如果不存在不添加
            if os.path.exists(Mod.Path):
                NeedDeleteMods.append(Mod)
        else:
            if os.path.exists(Mod.Path) is False:
                NeedDownloadMods.append(Mod)
            else:#文件存在 判断是否和服务端MD5相等 不等即损坏 需下载
                NeedCheckMod = filter(lambda x:os.path.split(x.Path)[1] == os.path.split(Mod.Path)[1], LocalMods)
                if not NeedCheckMod[0].MD5 == Mod.MD5:
                    NeedDeleteMods.append(NeedCheckMod)
                    NeedDownloadMods.append(Mod)
    #处理要删除的Mod
    for Mod in NeedDeleteMods:
        os.remove(Mod.Path)
    #处理要下载的Mod 关联进度条
    Q = mw.findChild(QtGui.QProgressBar,'JDT')
    for Mod in NeedDownloadMods:
        State.setText(os.path.split(Mod.Path)[1])
        crifanLib.downloadFile(Mod.Href,Mod.Path,True,Q,mapp)
    #更新完成提示框
    ConfirmDialog=QtGui.QMessageBox(mw)
    ConfirmDialog.setText(u"更新完成!")
    ConfirmDialog.setWindowTitle(u"提示")
    ConfirmDialog.setStandardButtons(QtGui.QMessageBox.Ok)
    ConfirmDialog.setButtonText(1,u"好")
    ConfirmDialog.setStyleSheet("background-color:#FFFFFF;")
    ConfirmDialog.exec_()
    State.setText(u"完毕,可以愉悦的启动游戏了")
    UpdaterConfig.Version = UpdaterConfig.ServerVersion
    #更新完成颜色还原
    mw.findChild(QtGui.QLabel,'NewVersion').setStyleSheet("QLabel{color:#98FB98;}")
    mw.findChild(QtGui.QLabel,'NowVersion').setText(u"当前客户端版本:"+UpdaterConfig.Version)
    crifanLib.saveBinDataToFile(json.dumps(vars(UpdaterConfig),sort_keys=True, indent=4),'Updater.json')
def InitClient():
    #判断Config是否存在,不存在写一个默认的进去
    if not os.path.exists('./Updater.json'):
        DefaultConfig = Updater.Updater("http://www.bigcraft.cn","Bigcraft",2333,"Bigcraft_0.1",False)
        crifanLib.saveBinDataToFile(json.dumps(vars(DefaultConfig),sort_keys=True, indent=4),'Updater.json')

    configFile = open('./Updater.json','r')
    #读取Config文件
    global UpdaterConfig
    UpdaterConfig = json.load(configFile,object_hook=Updater.ConvertUpdaterHook)
    configFile.close()
    UpdaterConfig.LoadServerInfo()
    UpdaterConfig.ServerImage()
    res = crifanLib.getUrlRespHtml_multiTry(UpdaterConfig.FilesAddress)

    for jsonobject in json.loads(res,object_hook=Mod.ConvertModHook):
        ServerMods.append(jsonobject)
    Helper.appendModInfo(LocalMods)

    mw.findChild(QtGui.QLabel,'NowVersion').setText(u"当前客户端版本:"+UpdaterConfig.Version)
    mw.findChild(QtGui.QLabel,'NewVersion').setText(u"最新客户端版本:"+UpdaterConfig.ServerVersion)

    for i in range(len(LocalMods)):
            LocalMods[i].Path = LocalMods[i].Path.decode("GB2312")
    if hasattr(UpdaterConfig,'Debug'):
        #crifanLib.saveBinDataToFile(json.dumps(list(LocalMods),sort_keys=True, indent=4,cls=Mod.PythonObjectEncoder),'LocalModsInfo.json')
        WriteJson = "[\n"
        for ModInfo in LocalMods:
            WriteJson += json.dumps(vars(ModInfo),sort_keys=True, indent=4)+
        WriteJson+="\n]"
        crifanLib.saveBinDataToFile(WriteJson,'LocalModsInfo.json')
        WriteJson = None
    
    Update(UpdaterConfig)
def Update(UpdaterConfig,IsCompulsory=False):
    if IsCompulsory is False:
        if UpdaterConfig.Version == UpdaterConfig.ServerVersion:
            return;
    State = mw.findChild(QtGui.QLabel,'State')
    State.setVisible(True)
    State.setText(u"检查新版本中...")
    mw.findChild(QtGui.QLabel,'NewVersion').setStyleSheet("QLabel{color:#D3391F;}")
    #需要更新
    ConfirmDialog=QtGui.QMessageBox(mw)
    ConfirmDialog.setText(u"发现客户端新版本:%s\n更新内容\n%s\n是否更新?"%(UpdaterConfig.ServerVersion,UpdaterConfig.Updates.strip().decode("UTF-8")))
    ConfirmDialog.setWindowTitle(u"发现新版本") 
    ConfirmDialog.setIcon(QtGui.QMessageBox.Information)
    ConfirmDialog.setStandardButtons(QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel)
    #ConfirmDialog.buttons.OK.setText(u"更更更更更踏马的")
    ConfirmDialog.setButtonText(1,u"更")
    ConfirmDialog.setButtonText(2,u"不更")
    #mw
    ConfirmDialog.setStyleSheet("background-color:#FFFFFF;")
    clicked = ConfirmDialog.exec_()
    if clicked == 1024:
        State.setText(u"更新前准备中...")
        U()
    else:
        State.setText(u"用户拒绝更新,已取消...")
class MainWindow(QtGui.QWidget):
    def __init__(self):
        
        QtGui.QWidget.__init__(self)
        
        #初始化position
        self.m_DragPosition=self.pos()
 
        self.resize(300,150)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setMouseTracking(True)
        self.setStyleSheet("background-color:#5C4978;")

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/Server.ico"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        #self.showEvent()
        #标题
        qlbl_Title = QtGui.QLabel(u"更新器",self)
        qlbl_Title.setGeometry(125,0,125,25)
        qlbl_Title.setStyleSheet("QLabel{color:#FF8C00;}")
        qlbl_Title.setObjectName("Title")
        #关闭按钮
        qbtn_Close=QtGui.QPushButton(u"×",self)
        qbtn_Close.setGeometry(275,0,25,25)
        qbtn_Close.setStyleSheet("QPushButton{background-color:#5C4978;border:none;color:#F50505;font-size:18px;font-weight:bold;}""QPushButton:hover{background-color:#333333;}")
        qbtn_Close.setObjectName("CloseBtn")
        #内容Panel
        qwgt_Panel = QtGui.QWidget(self)
        qwgt_Panel.setGeometry(QtCore.QRect(0,25,300, 125))
        qwgt_Panel.setStyleSheet("QWidget{background-color:#3B475E;}")
        #更新按钮
        qbtn_Update=QtGui.QPushButton(u"更新|修复",qwgt_Panel)
        qbtn_Update.setGeometry(195,50,80,30)
        qbtn_Update.setStyleSheet("QPushButton{background-color:#16A085;border:1px solid;color:#ffffff;font-size:13px;}""QPushButton:hover{background-color:#CE9178;}")
        qbtn_Update.clicked.connect(self.ReUpdate)
        qbtn_Update.setObjectName("UpdateBtn")
        #当前版本
        qlbl_NowVersion = QtGui.QLabel(u"当前客户端版本:Unknown",qwgt_Panel)
        qlbl_NowVersion.setGeometry(25,5,275,25)
        qlbl_NowVersion.setStyleSheet("QLabel{color:#98FB98;}")
        qlbl_NowVersion.setObjectName("NowVersion")
        #最新版本
        qlbl_NewVersion = QtGui.QLabel(u"最新客户端版本:Unknown",qwgt_Panel)
        qlbl_NewVersion.setGeometry(25,25,275,25)
        qlbl_NewVersion.setStyleSheet("QLabel{color:#98FB98;}")
        qlbl_NewVersion.setObjectName("NewVersion")
        #当前状态
        qlbl_State = QtGui.QLabel(u"更新完成",qwgt_Panel)
        qlbl_State.setGeometry(25,60,150,25)
        qlbl_State.setVisible(False)
        qlbl_State.setStyleSheet("QLabel{color:#98FB98;}")
        qlbl_State.setObjectName("State")
        #进度条
        qpbr_Size = QtGui.QProgressBar(qwgt_Panel)
        qpbr_Size.setGeometry(25, 90, 250, 25)
        qpbr_Size.setProperty("value", 100)
        qpbr_Size.setTextVisible(False)
        qpbr_Size.setObjectName("JDT")
        #注册事件
        self.connect(qbtn_Close,QtCore.SIGNAL("clicked()"),QtGui.qApp,QtCore.SLOT("quit()"))
    def showEvent(self,e):
        InitClient()
        #self.ReUpdate()
    def ReUpdate(self):
        Update(UpdaterConfig,True)
        #InitClient()
        #QtCore.QObject.findChild(QtGui.QLabel(),new QString("qlbl_Title"))
    #支持窗口拖动,重写两个方法
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_drag=True
            self.m_DragPosition=event.globalPos()-self.pos()
            event.accept()
 
    def mouseMoveEvent(self, QMouseEvent):
        if QMouseEvent.buttons() and Qt.LeftButton:
            self.move(QMouseEvent.globalPos()-self.m_DragPosition)
            QMouseEvent.accept()
 
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag=False

if __name__=="__main__":
    mapp=QtGui.QApplication(sys.argv)
    mw=MainWindow()
    mw.show()
    

    sys.exit(mapp.exec_())