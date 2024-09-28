"""
time:2023.3.13
author:wisdom
intruduction:程序与arduino进行串行通信，初始化上端机端口，
并向arduino发送舵机控制数据，并接收，分析超声波测距模块的数据，
并作出警示,无中断版本（使用中断效果不佳）
"""
import serial
import time
import os
#import music

def initConnection(portNo,baudRate):
    try:
        ser = serial.Serial(portNo,baudRate)#portNo:端口地址；baudRate：波特率
        print("Device Connectde")
        return ser
    except:
        print("Not Connectde")

def sendData(se,data,digits):
    myString = "$"
    for d in data:
        myString += str(d).zfill(digits)#25填充为025；
    try:
        se.write(myString.encode())
        print(myString)
    except:
        print("Data Transmission Failed!")

def control_dirction(ser,trach):
    if (trach==0):
        time.sleep(1)
        sendData(ser, [88, 000], 3)
        time.sleep(1)
        sendData(ser, [140, 000], 3)
        time.sleep(1)
        sendData(ser, [88, 000], 3)
        time.sleep(1)
    elif(trach==1):
        time.sleep(1)
        sendData(ser, [88, 90], 3)
        time.sleep(1)
        sendData(ser, [140, 90], 3)
        time.sleep(1)
        sendData(ser, [88, 000], 3)
        time.sleep(1)
    elif (trach == 2):
        time.sleep(1)
        sendData(ser, [88, 180], 3)
        time.sleep(1)
        sendData(ser, [140, 180], 3)
        time.sleep(1)
        sendData(ser, [88, 000], 3)
        time.sleep(1)
    else:
        time.sleep(1)
        sendData(ser, [88, -90], 3)
        time.sleep(1)
        sendData(ser, [140, -90], 3)
        time.sleep(1)
        sendData(ser, [88, 000], 3)
        time.sleep(1)

def rangeing(ser,flag):
    sendData(ser, [888, flag*100+flag*10+flag], 3)
    time.sleep(1)
    try:
        data = ser.read(1)#字符串
        print(data)
        time.sleep(1)
        data=int(data)
        if data!=0:#data==flag:
            print("warning!"+str(flag))
            os.system('play output.wav')
        else:
            print('prefect!')
    except: #serial.SerialTimeoutException:
        print("time out!")
    finally:
        ser.close()

def begin():#调用初始化
    ser = initConnection("/dev/ttyUSB0", 9600)  # linux
    #自检
    time.sleep(2)
    sendData(ser, [666, 666], 3)
    return ser

if __name__ =="__main__":
    #ser = initConnection("/dev/ttyUSB0",9600)#linux
    ser = initConnection("COM4",9600)#windows
    time.sleep(2)
    sendData(ser, [666, 666], 3)
    time.sleep(2)
    for i in range(4):
        control_dirction(ser, i)
