# -*- coding: utf-8 -*-
import sys, re, uuid
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import copy
import datetime
import dateutil.parser as parser
import arrow



# def removeColons(root):
#     ns = {'ead':'urn:isbn:1-931666-22-9'}
#     for el in root.iter('ead:*'):
#         fack=el.attrib
#         for x in fack:
#             attrText = fack[x]
#             if attrText.endswith(":"):
#                 fack[x] = attrText.replace(':','')
#                 # print(fack[x])
#
#     return root

def updateValues(root):



    infile_path = sys.argv[1]

    # time = datetime.now().strftime('%Y-%m-%d')
    #fix eadheader
    # print (root)
    #look for #### ####
    pattern1 = '\d{4}\s+\d{4}'
    #look for ##-##-#### ##-##-####
    pattern2 = '\d{2}-\d{2}-\d{4}\s\d{2}-\d{2}-\d{4}'
    for doc in root:

        for field in doc.findall("date"):

            if '-00-' in field.text:
                field.text = field.text.replace('-00-','')
            if '/00-' in field.text:
                field.text = field.text.replace('/00-','/')
            if '-00-00' in field.text:
                field.text = field.text.replace('-00-00','')
            #remove 00 from beginning of string
            if field.text.startswith('00'):
                field.text = field.text[2:]

            if field.text == 'None Given':
                doc.remove(field)
            # if '-00-00' in field.text:
            #
            #     field.text = field.text.replace('-00-00','')
            if ' ' in field.text:
                field.text = field.text.replace(' ','/')
            if '/' in field.text:
                date = field.text.split('/')
                date1=date[0]
                date2=date[1]


                if len(date1) == 7 and len(date2) == 7:
                    newdate1 = date1[3:]+'-'+date1[:2]
                    newdate2 = date2[3:]+'-'+date2[:2]
                    field.text=newdate1+'/'+newdate2


                if len(date1) == 10 and len(date2) == 7:

                        newdate1 = date1[6:]+'-'+date1[:2]+'-'+date1[3:5]
                        newdate2 = date2[3:]+'-'+date2[:2]
                        field.text=newdate1+'/'+newdate2

                if len(date1) == 7 and len(date2) == 10:
                        newdate1 = date1[3:]+'-'+date1[:2]
                        newdate2 = date2[6:]+'-'+date2[:2]+'-'+date2[3:5]
                        field.text=newdate1+'/'+newdate2

                if len(date1) == 10 and len(date2) == 10:
                        newdate1 = date1[6:]+'-'+date1[:2]+'-'+date1[3:5]
                        newdate2 = date2[6:]+'-'+date2[:2]+'-'+date2[3:5]
                        field.text=newdate1+'/'+newdate2

            else:
                #030-00117
                date = field.text
                if '-00-' in field.text:
                    field.text = field.text.replace('-00-','')
                    field.text = date[2:]+'-'+date[:2]
                if '/00-' in field.text:
                    field.text = field.text.replace('/00-','/')
                if '-00-00' in field.text:
                    field.text = field.text.replace('-00-00','')

                if field.text.startswith('00'):
                    field.text = field.text[2:]

                if re.search('[a-zA-Z]', field.text):
                    doc.remove(field)

                if len(date) == 7:
                    field.text = date[2:]+'-'+date[:2]
                if len(date) == 10:
                    field.text = date[6:]+'-'+date[:2]+'-'+date[3:5]
                if len(date) == 6:
                    field.text = date[2:]+'-'+date[:2]





        #
        # for field in doc.findall("date"):
            # print(field.text)
            # if re.search('[a-zA-Z]', field.text):
            #     doc.remove(field)
            # if '-00-' in field.text:
            #     field.text = field.text.replace('-00-','')
            # if '/00-' in field.text:
            #     field.text = field.text.replace('/00-','/')
            # if '-00-00' in field.text:
            #     field.text = field.text.replace('-00-00','')
            # #remove 00 from beginning of string
            # if field.text.startswith('00'):
            #     field.text = field.text[2:]
                # print(field.text)



    return root






def main():
    infile_path = sys.argv[1]
    outfile_path = 'rev_'+sys.argv[1]



    tree=ET.parse(infile_path)
    root=tree.getroot()
    # root.set('xmlns','urn:isbn:1-931666-22-9')
    # root.set('xmlns:xsi','http://www.w3.org/2001/XMLSchema-instance')
    # root.set('xsi:schemaLocation','urn:isbn:1-931666-22-9 https://www.loc.gov/ead/ead.xsd')
    # root.set('relatedencoding','MARC21')
    # print(root)
    updateValues(root)
    # removeColons(root)
    # updateAttributes(root)


    # print(tree)
    tree.write(outfile_path, xml_declaration=True,encoding='utf-8',method='xml')

# make this a safe-ish cli script
if __name__ == '__main__':
    # print(tree)

    main()
