import tensorflow as tf


def testGpu():#用来测试一下GPU环境
    if tf.test.gpu_device_name():
        print(f"Default GPU device: {tf.test.gpu_device_name()}")
    else:
        print("GPU device not found. Please check your settings.")

def update_transh_num(num):
    update_list=[]
    with open('update_transh_num.txt','r') as f:
        for each_line in f:
            update_list.append(int(each_line))
        if len(update_list)==0 or len(update_list)>=4:
            update_list = [0,0,0,0]
        update_list[num] = update_list[num]+1
    with open('update_transh_num.txt', 'w') as f:
        f.write(str(update_list[0]))
        for i in range(3):
            f.write('\n' + str(str(update_list[i+1])))

def rubbish2Classification(transh):
    #4个垃圾的分类表，发别是可回收垃圾，有害垃圾，厨余垃圾，其他垃圾
    recyclable_waste=['galss','metal','paper','plastic']
    kitchen_waste=['orange']
    other_waste=['wastePaper','palsticBag']
    hazardous_waste = ['battery']
    if (transh in recyclable_waste):
        return 0
    elif (transh in kitchen_waste):
        return 1
    elif (transh in other_waste):
        return 2
    else:
        return 3

if __name__ == '__main__':
    num=rubbish2Classification('glass')
    print(num)

