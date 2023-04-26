import os
import re
import uuid
import glob
import openai
import xml.etree.ElementTree as ET

from pathlib import Path
from os import listdir
from os.path import isfile, join
from xml.etree.ElementTree import Element, SubElement, Comment, tostring

openai.api_key = ''

metadata = []
basedir = '/Users/erra1244/Desktop/codaily/issues_XML/'
rows = ['test']

bibData = {}

for mydir in os.listdir(basedir):
    if os.path.isdir(os.path.join(basedir, mydir)):
        row = []
        for myfile in os.listdir(os.path.join(basedir, mydir)):
            # if 'mets' not in myfile:
            #     result = os.path.join(basedir, mydir, myfile)
            #     xml = open(result, 'r')
            #     tree = ET.parse(xml)
            #     root = tree.getroot()
            #     thing = ''
            #     for tag in root.findall('.//*[@CONTENT]'):
            #         x = tag.attrib['CONTENT'] + ' '
            #         thing += x
            #     bibData['ocr'] = thing

                
        		
            if 'mets' in myfile:
            	result = os.path.join(basedir, mydir, myfile)
            	bibxml = open(result, 'r')
            	tree = ET.parse(bibxml)
            	root = tree.getroot()
            	ns = {'mets':'http://www.loc.gov/METS','mods':'http://www.loc.gov/mods/v3'}
            	if ET.ParseError:
            		print(myfile)
            	# for x in root:
            	# 	thing=x
        		
            		
            	# print(myfile)
            	# for title in root.findall('mods:title',ns):
            	# 	print(title.text)

# print(bibData)

# write_csv(rows)

# path = Path("/Users/erra1244/Desktop/issues_XML/")
# for file in path.glob("./*"):
# 	print(file)
        # with open(file,'r') as xmlFile:
        #     tree = ET.parse(xmlFile)
        #     root = tree.getroot()

# p = Path("/Users/erra1244/Desktop/Issues_XML/")

# file_list = [f for f in p.iterdir() if f.is_file()]


# for folder in p.glob('*'):
# 	print (folder)


	# file = sys.argv[1]
	# ns = {'alto':'http://www.loc.gov/standards/alto/ns-v2#'}




# with open(outfile_path, 'w') as resultsFile:
#         field_names=['title', 'ocr']


#         writer = csv.DictWriter(resultsFile, field_names, extrasaction='ignore',lineterminator='\n')
#         writer.writeheader()
#         for out_row in out_rows:
#             writer.writerow(out_row)



	
