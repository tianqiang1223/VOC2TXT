import os
from xml.dom import minidom
from os.path import join

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x, y, w, h)

def convert_annotation(sets, image_set_dir, image_path, save_txt_dir, save_label_dir, xml_dir, classes):
    for image_set in sets:
        image_ids = open(image_set_dir + '/%s.txt' % (image_set)).read().strip().split()
        list_file = open(save_txt_dir+ '/%s.txt' % (image_set), 'w')
        for image_id in image_ids:
            list_file.write(image_path + '/%s.jpg\n' % (image_id))
            in_file = open(xml_dir + '/%s.xml' % (image_id), encoding='utf-8')
            out_file = open(save_label_dir + '/%s.txt' % (image_id), 'w', encoding='utf-8')

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
    classes = ['face', 'person']
    
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
