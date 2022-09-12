import xml.etree.ElementTree as ET
from lxml import etree

    
import os

def find_rec(elem, result):
    for child in elem.getchildren():
        result.append(child.tag)
        find_rec(child, result)


def get_xml_text(path):
    parser = etree.XMLParser(recover=True,encoding='utf-8')
    xml = ET.parse(path,parser=parser).getroot()


    elem_list = []
    # find_rec(xml, elem_list)
    # print(elem_list)

    print(xml.tag)

    print('-')
    for e in xml:
        print(e.tag, e.attrib, e.text)

    # elem_list = list(set(elem_list))
    # print(elem_list)

    # print(ET.tostring(xml_file.getroot(), encoding='utf-8', method='text'))


if __name__ == '__main__':
    folder_path = 'xml/'
    paths = [folder_path + p for p in os.listdir(folder_path)]

    p1 = paths[0]
    print(p1)

    get_xml_text(p1)
