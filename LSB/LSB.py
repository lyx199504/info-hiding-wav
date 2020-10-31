#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/10/23 16:16
# @Author : LYX-夜光

from array import array

# 文件转字节数组
def file2byte(fileName, start=0):
    with open(fileName, "rb") as file:
        head = file.read(start)
        byteList = array('H', (0 for _ in range((file.seek(0, 2)-start)//2)))
        file.seek(start)
        file.readinto(byteList)
    return head, byteList

# 字节数组转文件
def byte2file(fileName, byteList, head=None):
    with open(fileName, "wb") as file:
        if head:
            file.write(head)
        byteList.tofile(file)

# LSB隐写术
def LSBHiding(carrier, message, stego):
    # 获取wav文件的头部字节（前44字节）和数据字节
    head, cList = file2byte(carrier, 44)
    _, mList = file2byte(message)  # 获取秘密信息字节
    n = 16
    for i in range(len(mList)):
        b = '{:016b}'.format(mList[i])
        for j in range(n):
            cList[i*n+j] += (int(b[j]) - cList[i*n+j]%2)
    byte2file(stego, cList, head)

# LSB提取
def LSBExtract(stego, message):
    _, sList = file2byte(stego, 44)
    n = 16
    byteList = array('H')
    byte = 0
    for i in range(len(sList)):
        if i%n == 0:
            byte = sList[i]%2
        else:
            byte = byte*2+sList[i]%2
            if i%n == n-1:
                byteList.append(byte)
    print("s", byteList[:23])
    byte2file(message, byteList[:23])

if __name__ == "__main__":
    LSBHiding("carrier.wav", "hidden.txt", "stego.wav")
    LSBExtract("stego.wav", "message.txt")