import xml
print(xml.__file__)

from xml.dom import minidom 
import xml.etree.ElementTree as ET

import os  
  
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
    #to browse how xml appeare
    parent_tree = ET.parse(save_path_file)
    parent = parent_tree.getroot()
    xmlstr = minidom.parseString(ET.tostring(parent)).toprettyxml()
    print (xmlstr)
