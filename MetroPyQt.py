#!/usr/bin/env python
# -*- coding:utf-8 -*-
 
#system imports
import sys
 
#pyqt imports
from PyQt4 import QtCore,QtGui
from PyQt4.QtCore import Qt

class MainWindow(QtGui.QWidget):
    def __init__(self):
 
        QtGui.QWidget.__init__(self)
 
        #初始化position
        self.m_DragPosition=self.pos()
 
        self.resize(300,150)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setMouseTracking(True)
        self.setStyleSheet("background-color:#5C4978;")
 
        qwgt_Panel = QtGui.QWidget(self)
        qwgt_Panel.setGeometry(QtCore.QRect(0,25,300, 125))
        qwgt_Panel.setStyleSheet("QWidget{background-color:#3B475E;}")
        #按钮一
        qbtn_Update=QtGui.QPushButton(u"更新|修复",qwgt_Panel)
        qbtn_Update.setGeometry(200,30,80,30)
        qbtn_Update.setStyleSheet("QPushButton{background-color:#16A085;border:1px solid;color:#ffffff;font-size:15px;}""QPushButton:hover{background-color:#333333;}")
        qbtn_Update.clicked.connect(self.showDialog)
        qbtn_Close=QtGui.QPushButton(u"×",self)
        qbtn_Close.setGeometry(275,0,25,25)
        qbtn_Close.setStyleSheet("QPushButton{background-color:#5C4978;border:none;color:#F50505;font-size:15px;}""QPushButton:hover{background-color:#333333;}")

        qlbl_Title = QtGui.QLabel(u"更新器",self)
        qlbl_Title.setGeometry(125,0,125,25)
        qlbl_Title.setStyleSheet("QLabel{color:#FF8C00;}")
        #注册事件
        self.connect(qbtn_Close,QtCore.SIGNAL("clicked()"),QtGui.qApp,QtCore.SLOT("quit()"))
    def showDialog(self):
        print "AAA"
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