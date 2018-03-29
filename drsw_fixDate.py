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
        for field in doc.findall("field[@name='date_t']"):


            if field.text == 'None Given':
                doc.remove(field)
            if field.text == 'None/Given':
                doc.remove(field)

            if ' ' in field.text:
                field.text = field.text.replace(' ','/')
                # print(field.text)
            if re.search(pattern1, field.text):
                field.text = field.text.replace(' ','/')
        #
        # for field in doc.findall("field[@name='date_t']"):
        #     # print(field.text)
        #     if re.search('[a-zA-Z]', field.text):
        #         doc.remove(field)
        #     if '-00-' in field.text:
        #         field.text = field.text.replace('-00-','')
        #     if '/00-' in field.text:
        #         field.text = field.text.replace('/00-','/')
        #     #remove 00 from beginning of string
        #     if field.text.startswith('00'):
        #         field.text = field.text[2:]
        #         # print(field.text)

        for field in doc.findall("field[@name='date_t']"):
            # print(field.text)
            if '/' in field.text:
                date= field.text.split('/')
                # print(date)
                for x in date:

                    if len(x) == 7:
                    #
                        field.text = x[2:]+'-'+x[:2]
                    #     print(newx)

                    if len(x) == 10:

                        newx = x[6:]+'-'+x[:2]+'-'+x[3:5]
                        # print(newx)
                        field.text=newx
            else:
                date = field.text
                # print(date)
                if len(date) == 7:
                    field.text = date[2:]+'-'+date[:2]

                if len(date) == 10:
                    print(date)
                #
                #         newx = x[6:]+'-'+x[:2]+'-'+x[3:5]
                #         # print(newx)
                #         field.text=newx

                    #     # x = x.replace(x,x[6:]+'-'+x[:2]+'-'+x[3:5])
                    #     field.text=newx
                        # print(field.text)

                        # return x
                        # year
                        # print(x[6:])
                        # day
                        # print(x[3:5])
                        # month
                        # print(x[:2])


                        # print(x)




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
