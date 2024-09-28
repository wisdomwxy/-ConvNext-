This program uses a trained ConvNext neural network for garbage classification. The camera senses the garbage placed on the feeding platform and transmits the collected information into the neural network, and then the result is judged based on the output of the neural network, and the corresponding servo is controlled by Arduino to complete the corresponding action.
本程序使用训练好的ConvNext神经网络进行垃圾分类。由摄像头感知被放置在投料平台的垃圾，并将采集的信息传入神经网络，然后根据神经网络的输出判别结果，arduino控制相应舵机完成相应的动作。

在程序同级目录下，你必须创建3文件夹cap_photos save_weigth test,分别用来储存拍摄的照片，保存训练好的权重，和测试集合图片
In the same level directory of the program, you must create three folders named "cap_photos", "save_weigth", and "test", respectively, to store the captured photos, save the trained weight, and test set images.

权重文件和训练数据集需要自己下载或创建，目录结构为：
The weight file and training dataset need to be downloaded or created by yourself, and the directory structure is:

main.py
cap_photos
save_weigth
weigth files
test
...
data_set\junk\xxx.jpg
