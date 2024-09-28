"""
intruduction:相机测试函数
"""

import cv2
import os

def count_files_in_directory(directory):
    """
    计算指定文件夹中的文件数量（不包括子文件夹中的文件）。
    """
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if os.path.isfile(os.path.join(root, file)):
                count += 1
    return count

def create_data_set(output_dir):
    camera = cv2.VideoCapture(0)  # 摄像头序号
    cv2.namedWindow('Video_Cam', cv2.WINDOW_NORMAL)
    count=count_files_in_directory(output_dir)
    while cv2.waitKey(1) != 27:  # esc退出
        success, frame = camera.read()
        cv2.imshow('Video_Cam', frame)
        if cv2.waitKey(1) == 32:  # space拍照

            print("cap_ing!")
            count = count + 1
            print(output_dir + r'\battery_' + str(count) + '.jpg')
            file_name = str(output_dir + r'\battery_' + str(count) + '.jpg')
            cv2.imwrite(file_name, frame)

    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    create_data_set(r"D:\pyc_workspace\TF2.11\data_set\Junk_data_sets\orange")