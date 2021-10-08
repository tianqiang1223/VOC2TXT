import os
from xml.dom import minidom
from os.path import join

# 归一化
def convert(size, box):         # size:(原图w,原图h) , box:(xmin,xmax,ymin,ymax)
    dw = 1./size[0]             # 1/w
    dh = 1./size[1]             # 1/h
    x = (box[0] + box[1])/2.0   # 物体在图中的中心点x坐标
    y = (box[2] + box[3])/2.0   # 物体在图中的中心点y坐标
    w = box[1] - box[0]         # 物体实际像素宽度
    h = box[3] - box[2]         # 物体实际像素高度
    x = x*dw                    # 物体中心点x的坐标比(相当于 x/原图w)
    w = w*dw                    # 物体宽度的宽度比(相当于 w/原图w)
    y = y*dh                    # 物体中心点y的坐标比(相当于 y/原图h)
    h = h*dh                    # 物体宽度的宽度比(相当于 h/原图h)
    return (x, y, w, h)         # 返回相对于原图的物体中心点的x坐标比,y坐标比,宽度比,高度比 [0-1]

def convert_annotation(sets, image_set_dir, image_path, save_txt_dir, save_label_dir, xml_dir, classes):
    '''
    将对应文件名的xml文件转化为label文件，xml文件包含了对应的bunding框以及图片长款大小等信息，
    通过对其解析，然后进行归一化最终读到label文件中去，也就是说
    一张图片文件对应一个xml文件，然后通过解析和归一化，能够将对应的信息保存到唯一一个label文件中去
    labal文件中的格式：calss x y w h 同时，一张图片对应的类别有多个，所以对应的bunding的信息也有多个
    '''
    for image_set in sets:
        image_ids = open(image_set_dir + '/%s.txt' % (image_set)).read().strip().split()
        list_file = open(save_txt_dir+ '/%s.txt' % (image_set), 'w')
        for image_id in image_ids:
            list_file.write(image_path + '/%s.jpg\n' % (image_id))
            in_file = open(xml_dir + '/%s.xml' % (image_id), encoding='utf-8')
            out_file = open(save_label_dir + '/%s.txt' % (image_id), 'w', encoding='utf-8')
            
            # 解析xml文件
            dom=minidom.parse(in_file)
            root=dom.documentElement
    
            width = root.getElementsByTagName('width')[0].childNodes[0].data
            height = root.getElementsByTagName('height')[0].childNodes[0].data
            w = float(width)
            h = float(height)
            
            objects = root.getElementsByTagName('object')
            for object in objects:
                name = object.getElementsByTagName('name')[0].childNodes[0].data
                xmin = object.getElementsByTagName('xmin')[0].childNodes[0].data
                xmax = object.getElementsByTagName('xmax')[0].childNodes[0].data
                ymin = object.getElementsByTagName('ymin')[0].childNodes[0].data
                ymax = object.getElementsByTagName('ymax')[0].childNodes[0].data
                xmin, xmax, ymin, ymax = float(xmin), float(xmax), float(ymin), float(ymax)
                name_id = classes.index(name)
                xywh = convert((w, h), (xmin, xmax, ymin, ymax))
                out_file.write(str(name_id) + " " + " ".join([str(x) for x in xywh]) + '\n')

def main():
    sets = ['train', 'test', 'val']
    classes = ['face', 'person', 'belt', 'smoke', 'phone', 'distraction', 'eye_open', 'eye_close', 'mouth_open', 'mouth_close']
    
    image_set_dir = 'data/ImageSets'
    xml_dir = 'data/Annotations'
    image_path = 'data/images'
    save_txt_dir = 'data'
    save_label_dir = 'data/labels'

    if not os.path.exists(save_label_dir):
        os.makedirs(save_label_dir)
    
    convert_annotation(sets, image_set_dir, image_path, save_txt_dir, save_label_dir, xml_dir, classes)

if __name__ == '__main__':
    main()
