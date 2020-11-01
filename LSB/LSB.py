#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/10/23 16:16
# @Author : LYX-夜光

from array import array

# 文件转字节数组
def file2byte(fileName, start=0, bit=8):
    with open(fileName, "rb") as file:
        head = file.read(start)
        if bit == 16:
            byteList = array('H', (0 for _ in range((file.seek(0, 2)-start)//2)))
        else:
            byteList = array('B', (0 for _ in range((file.seek(0, 2)-start))))
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
    wavBit = 16  # 音频采样深度为16位
    msgBit = 8  # 秘密信息按照一个字节编码
    # 获取wav文件的头部字节（前44字节）和数据字节
    head, cList = file2byte(carrier, 44, wavBit)
    _, mList = file2byte(message)  # 获取秘密信息字节
    c10len, m10len = len(cList), len(mList)
    m2len = m10len*msgBit
    m = len('{:b}'.format(c10len))  # 音频字节长度的二进制长度，前m位LSB用来表示可存储秘密信息的最大长度
    if c10len - m < m2len:  # 音频可存储的位数小于秘密信息的位数
        return False
    # 音频的前m位LSB存储秘密信息的长度
    b = ('{:0'+str(m)+'b}').format(m2len)  # 秘密信息的长度转二进制
    for j in range(m):
        cList[j] += (int(b[j]) - cList[j]%2)
    # 音频在第m位LSB之后存储秘密信息
    for i in range(m10len):
        b = ('{:0'+str(msgBit)+'b}').format(mList[i])  # 秘密信息字节转为二进制
        for j in range(msgBit):
            cList[m+i*msgBit+j] += (int(b[j]) - cList[m+i*msgBit+j]%2)
    byte2file(stego, cList, head)
    return True

# LSB提取
def LSBExtract(stego, message):
    wavBit = 16  # 音频采样深度为16位
    msgBit = 8  # 秘密信息按照一个字节编码
    _, sList = file2byte(stego, 44, wavBit)
    s10len = len(sList)
    m = len('{:b}'.format(s10len))  # 这里的m同上
    byteList = array('B')
    m2len = 0  # 秘密信息的长度
    for i in range(m):
        m2len = m2len*2 + sList[i]%2
    # 提取秘密信息
    byte = 0
    for i in range(m2len):
        if i%msgBit == 0:
            byte = sList[m+i]%2
        else:
            byte = byte*2+sList[m+i]%2
            if i%msgBit == msgBit-1:
                byteList.append(byte)
    byte2file(message, byteList)

if __name__ == "__main__":
    LSBHiding("carrier.wav", "hidden.txt", "stego.wav")
    LSBExtract("stego.wav", "message.txt")