"""
time:2024.4.22
author:wisdom
intruduction:
基于predict.py增加了一个函数update_transh_num(num)
该函数用于存储分类垃圾的历史，每次启动重置所有垃圾数量为0，垃圾种类为4
每次识别成功将数据写入update_transh_num.txt
"""
import os
import json
import glob
import numpy as np

from PIL import Image
import tensorflow as tf
import matplotlib.pyplot as plt

from model import convnext_tiny as create_model

from cap import cap_transh,get_img

def main(cap_img_path):
    num_classes = 7
    im_height = im_width = 224


    # load image

    img_path = cap_img_path
    # testGlass.jpg testMetal.jpg testPlastic.jpg testPaper.jpg testTrash.jpg
    assert os.path.exists(img_path), "file: '{}' dose not exist.".format(img_path)
    img = Image.open(img_path)
    # resize image
    img = img.resize((im_width, im_height))
    plt.imshow(img)

    # read image
    img = np.array(img).astype(np.float32)

    # preprocess
    img = (img / 255. - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]

    # Add the image to a batch where it's the only member.
    img = (np.expand_dims(img, 0))

    # read class_indict
    json_path = './class_indices.json'
    assert os.path.exists(json_path), "file: '{}' dose not exist.".format(json_path)

    with open(json_path, "r") as f:
        class_indict = json.load(f)

    # create model
    model = create_model(num_classes=num_classes)
    model.build([1, 224, 224, 3])

    weights_path = './save_weights/model.ckpt'
    assert len(glob.glob(weights_path+"*")), "cannot find {}".format(weights_path)
    model.load_weights(weights_path)

    result = np.squeeze(model.predict(img, batch_size=1))
    result = tf.keras.layers.Softmax()(result)
    predict_class = np.argmax(result)

    print_res = "class: {}   prob: {:.3}".format(class_indict[str(predict_class)],
                                                 result[predict_class])
    print('<-------分类结果------->')
    print(print_res)
    print('<------------------------->')


    transh_list=[predict_class,class_indict[str(predict_class)]]
    return transh_list

def update_transh_num(num):
    update_list = []
    with open('update_transh_num.txt', 'r') as f:
        for each_line in f:
            update_list.append(int(each_line))
        if len(update_list) != 4:
            update_list = [0, 0, 0, 0]
        update_list[num] = update_list[num] + 1
    with open('update_transh_num.txt', 'w') as f:
        f.write(str(update_list[0]))
        for i in range(3):
            f.write('\n' + str(str(update_list[i + 1])))

def rubbish2Classification(transh):
    #4个垃圾的分类表，发别是可回收垃圾，有害垃圾，厨余垃圾，其他垃圾0
    recyclable_waste=['galss','metal','paper','plastic']
    kitchen_waste=['orange']
    other_waste=['transh']
    hazardous_waste = ['battery']
    if (transh in recyclable_waste):
        return 0
    elif (transh in kitchen_waste):
        return 1
    elif (transh in other_waste):
        return 2
    elif (transh in hazardous_waste):
        return 3


if __name__ == '__main__':
    cap_transh(r"D:\pyc_workspace\TF2.11\cap_photos",1)
    file_name=get_img()
    transh=main(file_name)
    update_transh_num(rubbish2Classification(transh[1]))
    print(transh)
