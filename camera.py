"""
time:2024.4.22
author:wisdom
intruduction:相机测试函数，可以直接看视频流确定要拍摄的垃圾位置
"""

import cv2
import os

def cap_transh(output_dir,flag=1):
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
    cv2.namedWindow('Video_Cam', cv2.WINDOW_NORMAL)
    while cv2.waitKey(1) != 27:  # esc退出
        success, frame = camera.read()
        cv2.imshow('Video_Cam', frame)
        if cv2.waitKey(1) == 32:  # space拍照
            print("cap_ing!")
            num_max  = num_max  + 1
            print(output_dir+r'\cap_'+str(num_max)+'.jpg')
            file_name = str(output_dir+r'\cap_'+str(num_max)+'.jpg')
            cv2.imwrite(file_name,frame)

    camera.release()
    cv2.destroyAllWindows()

    with open('num_of_cap.txt', 'a') as f:
        if len(num)==0:
            f.write(str(num_max))
        else:
            f.write('\n' + str(num_max))



if __name__ == '__main__':
    cap_transh(r"D:\pyc_workspace\TF2.11\cap_photos",0)
