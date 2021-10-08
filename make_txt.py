import os
import random

def create_txt(xml_dir, save_txt_dir, trainval_precent=0.9, train_precent=0.9):
    xml_file = os.listdir(xml_dir)
    num = len(xml_file)
    xml_num_list = range(num)
    tv_num = int(num * trainval_precent)
    tr_num = int(tv_num * train_precent)
    trainval = random.sample(xml_num_list, tv_num)
    train = random.sample(trainval, tr_num)

    ftrainval = open(save_txt_dir + '/trainval.txt', 'w')
    ftrain = open(save_txt_dir + '/train.txt', 'w')
    fval = open(save_txt_dir + '/val.txt', 'w')
    ftest = open(save_txt_dir + '/test.txt', 'w')

    for i in xml_num_list:
        name = xml_file[i][:-4] + '\n'
        if i in trainval:
            ftrainval.write(name)
            if i in train:
                ftrain.write(name)
            else:
                fval.write(name)
        else:
            ftest.write(name)
    ftrainval.close()
    ftrain.close()
    fval.close()
    ftest.close()

def main():
    trainval_precent = 0.9
    train_precent = 0.9
    xml_dir = 'data/Annotations'
    save_txt_dir = 'data/ImageSets'
    if not os.path.exists(save_txt_dir):
        os.makedirs(save_txt_dir)
    create_txt(xml_dir, save_txt_dir, trainval_precent, train_precent)

if __name__ == '__main__':
    main()
