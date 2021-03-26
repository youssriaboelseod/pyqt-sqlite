__author__ = 'youssri Ahmed Hamdy <estratigy@yahoo.com>'
__copyright__ = 'Copyright (c) 2021'
__version__ = '1.0.0'

import xml
print(xml.__file__)

from xml.dom import minidom 
import xml.etree.ElementTree as ET

import os  
TYPE_relation={1:"alone field with new columns",2:"related field with previews columns"}
TYPE_API={1:"field",2:"drop list",3:"title"}

def create_xml(name):  
    root = minidom.Document()     
    xml = root.createElement('root')  
    root.appendChild(xml) 
    productChild = root.createElement('product') 
    productChild.setAttribute('name', 'Geeks for Geeks') 
    xml.appendChild(productChild) 
    xml_str = root.toprettyxml(indent ="\t")  
    save_path_file = name+".xml"
    with open(save_path_file, "w") as f: 
        f.write(xml_str)  
    #to print  xml in terminal
    parent_tree = ET.parse(save_path_file)
    parent = parent_tree.getroot()
    xmlstr = minidom.parseString(ET.tostring(parent)).toprettyxml()
    print (xmlstr)

def addUi(formName,newForm=True,newField=True,linkRelated=True):  
    if newForm:
        create_xml(formName)
    if newField:
       print("adding xml field")

    if linkRelated:
        pass
