"""
time:2024.4.22
author:wisdom
intruduction:
1.启动摄像头拍照并按序列命名，最后储存指定路径
2.返回最新图片路径地址
会产生两个配置文件：
num_of_cap.txt：图片序列存放索引
D:\pyc_workspace\TF2.11\cap_photos：图片存放路径
"""

import cv2
import os

def cap_transh(output_dir,flag=1):#flag=1正常拍照，非1清除数据
    if flag != 1:
        with open('num_of_cap.txt', 'w') as f:
            for file in os.listdir(output_dir):
                # 构建文件的完整路径
                file_path = os.path.join(output_dir, file)
                # 如果是文件，则删除
                os.remove(file_path)
                print("已删除文件:", file_path)
            print("！清除所有内容！")

    num = []
    with open('num_of_cap.txt','r') as f:
        for each_line in f:
            num.append(int(each_line))
    print(num)
    if len(num)==0:
        num_max=0
    else:
        num_max = max(num)

    camera = cv2.VideoCapture(0)  # 摄像头序号
    if not camera.isOpened():
        print("无法打开摄像头")
        return
    success, frame = camera.read()
    camera.release()
    print("cap_ing!")
    num_max  = num_max  + 1
    print(output_dir+r'\cap_'+str(num_max)+'.jpg')
    file_name = str(output_dir+r'\cap_'+str(num_max)+'.jpg')
    cv2.imwrite(file_name,frame)

    with open('num_of_cap.txt', 'a') as f:
        if len(num)==0:
            f.write(str(num_max))
        else:
            f.write('\n' + str(num_max))

def get_img():
    num=[]
    output_dir=r"D:\pyc_workspace\TF2.11\cap_photos"
    with open('num_of_cap.txt','r') as f:
        for each_line in f:
            num.append(int(each_line))
    print(num)
    if len(num)==0:
        num_max=0
    else:
        num_max = max(num)
    file_name = str(output_dir+r'\cap_'+str(num_max)+'.jpg')
    #返回照片的地址
    return file_name



if __name__ == '__main__':
    cap_transh(r"D:\pyc_workspace\TF2.11\cap_photos")
    str = get_img()
    print(str)
