#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/10/31 20:59
# @Author : LYX-夜光

from PyQt5 import QtWidgets
from LSB import LSB

class Photo(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.carrier = None
        self.message = None
        self.stego = None
        self.message_ = None
        self.setWindow()

    def setWindow(self):
        self.winWidth, self.winHeight = 500, 250
        self.resize(self.winWidth, self.winHeight)  # 设置窗口大小
        self.setWindowTitle("音频信息隐藏（夜光制作）")

        buWidth, buHeight = self.winWidth / 3, self.winHeight / 3  # 按钮大小
        leftWidth, upHeight = self.winWidth/4 - buWidth/2, self.winHeight/4 - buHeight/2
        rightWidth, downHeight = leftWidth + self.winWidth/2, upHeight + self.winHeight/2

        # 打开音频文件
        button1 = QtWidgets.QPushButton("选择音频文件", self)
        button1.resize(buWidth, buHeight)
        button1.move(leftWidth, upHeight)
        button1.clicked.connect(self.getCoverFile)
        # 打开信息文件
        button2 = QtWidgets.QPushButton("选择信息文件", self)
        button2.resize(buWidth, buHeight)
        button2.move(rightWidth, upHeight)
        button2.clicked.connect(self.getMessageFile)
        # 隐藏
        button3 = QtWidgets.QPushButton("隐藏", self)
        button3.resize(buWidth, buHeight)
        button3.move(leftWidth, downHeight)
        button3.clicked.connect(self.setStegoFile)
        # 提取
        button4 = QtWidgets.QPushButton("提取", self)
        button4.resize(buWidth, buHeight)
        button4.move(rightWidth, downHeight)
        button4.clicked.connect(self.setMessageFile)

    # 打开音频文件
    def getCoverFile(self):
        self.carrier = QtWidgets.QFileDialog.getOpenFileName(self, "选择音频文件", "./", "Wav Files (*.wav)")[0]  # 打开文件获取链接
        if self.carrier:
            self.stego = self.carrier  # 打开音频文件也可用于提取隐藏信息
            QtWidgets.QMessageBox.about(self, "温馨提示", "选择音频文件成功！")

    # 打开信息文件
    def getMessageFile(self):
        self.message = QtWidgets.QFileDialog.getOpenFileName(self, "打开信息文件")[0]  # 打开文件获取链接
        if self.message:
            QtWidgets.QMessageBox.about(self, "温馨提示", "选择信息文件成功！")

    # 保存隐藏文件
    def setStegoFile(self):
        if not self.carrier:
            QtWidgets.QMessageBox.about(self, "温馨提示", "请先选择音频文件！")
        elif not self.message:
            QtWidgets.QMessageBox.about(self, "温馨提示", "请先选择信息文件！")
        else:
            self.stego = QtWidgets.QFileDialog.getSaveFileName(self, "保存隐藏文件", "./", "Wav Files (*.wav)")[0]
            if self.stego:
                try:
                    success = LSB.LSBHiding(self.carrier, self.message, self.stego)
                    if success:
                        QtWidgets.QMessageBox.about(self, "温馨提示", "隐藏成功！")
                    else:
                        QtWidgets.QMessageBox.about(self, "温馨提示", "隐藏失败，信息文件超过音频文件可存储位数！")
                    self.carrier = self.message = None
                except:
                    QtWidgets.QMessageBox.about(self, "温馨提示", "隐藏失败！")

    # 保存提取文件
    def setMessageFile(self):
        if not self.stego:
            QtWidgets.QMessageBox.about(self, "温馨提示", "请先选择音频文件！")
        else:
            print(self.stego)
            self.message_ = QtWidgets.QFileDialog.getSaveFileName(self, "保存提取文件")[0]
            if self.message_:
                try:
                    LSB.LSBExtract(self.stego, self.message_)
                    QtWidgets.QMessageBox.about(self, "温馨提示", "提取成功！")
                    self.message_ = self.stego = None
                except:
                    QtWidgets.QMessageBox.about(self, "温馨提示", "提取失败！")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    photo = Photo()
    photo.show()
    app.exec_()