# -*- coding: utf-8 -*-
import sys, re, uuid
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import copy
import datetime
import dateutil.parser
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
        # for field in doc.findall("field[@name='date_t']"):
        #
        #     if field.text == 'None Given':
        #         doc.remove(field)
        #     if field.text == 'None/Given':
        #         doc.remove(field)
        #
        #     if ' ' in field.text:
        #         field.text = field.text.replace(' ','/')
        #         # print(field.text)
        #     if re.search(pattern1, field.text):
        #         field.text = field.text.replace(' ','/')

        for field in doc.findall("field[@name='date_t']"):
            if re.search('[a-zA-Z]', field.text):
                doc.remove(field)
            if '-00-' in field.text:
                field.text = field.text.replace('-00-','')
            if '/00-' in field.text:
                field.text = field.text.replace('/00-','/')
            if field.text.startswith('00'):
                print(field.text)
                # field.text.replace('00','')

        # for field in doc.findall("field[@name='date_t']"):
        #     if '/' in field.text:
        #         date= field.text.split('/')
        #         for x in date:
        #             if len(x) == 6:
        #                 # print(x)
        #                 newx=datetime.datetime.strptime(x, "%m%Y").strftime("%Y-%m")
        #                 print(newx)
        # print(field.text)

            # if field.text
    # header=root.find('ead:eadheader', ns)
    # # print(header.tag)
    # header.set('findaidstatus','complete')
    # # print(header.attrib)
    #
    #
    # revision=SubElement(header, 'revisiondesc')
    # change=SubElement(revision,'change')
    # revDate=SubElement(change,'date')
    # revDate.set('normal', time)
    # revDate.text = time
    # item = SubElement(change, 'item')
    # item.text = 'This finding aid was updated in alignment with LC EAD 2.0 specifications using a python script created by Erik Radio.'
    #
    # #fix EADid
    # EADid = header.find('ead:eadid',ns)
    # EADid.text=infile_path.strip('.xml')
    #
    #
    #
    #
    #
    # #date
    #
    # pubDate = header.find('ead:filedesc/ead:publicationstmt/ead:date',ns)
    # pubDate.text = pubDate.text.replace(u"© ","")
    # pubDate.text = pubDate.text.replace("; ","")
    #
    # #control access to remove list
    # conAcc = root.find('ead:archdesc/ead:controlaccess',ns)
    # # print(conAcc)
    # subj=[]
    # for thing in conAcc.findall('ead:list/ead:item/*',ns):
    #     subj.append(thing)
    #     # print(subj)
    #     for head in conAcc.findall('ead:head',ns):
    #         print(head.tag)
    #         conAcc.remove(head)
    #     for y in conAcc.findall('ead:list',ns):
    #         conAcc.remove(y)
    #
    # for x in subj:
    #
    #     newsubj = SubElement(conAcc,x.tag)
    #     newsubj.text=x.text

    return root


# def updateAttributes(root):
#     ns = {'ead':'urn:isbn:1-931666-22-9'}
#     header=root.find('ead:eadheader',ns)
#
#     repoCode=root.find('ead:archdesc/ead:did/ead:unitid',ns)
#     repoCode.set('repositorycode','US-azu')
#     repoCode.set('countrycode','US')
#     # print(repoCode.attrib)
#
#     for repoDate in root.iter('ead:unitdate'):
#         date=repoDate.attrib
#         if date == '':
#             date.attrib.pop('normal', None)
#         if date == 'NaN':
#             date.attrib.pop('normal', None)
#         if date == 'AzU':
#             date.attrib.pop('normal', None)
#         # print(date)
#     # print(repoDate)
#
#     archDesc=root.find('ead:archdesc',ns)
#     # print(archDesc)
#     archDesc.attrib.pop('relatedencoding', None)
#     archDesc.set('encodinganalog','351$c')
#
#     #langmaterial
#     langusage = header.find('ead:profiledesc/ead:langusage/ead:language',ns)
#     langusage.set('langcode','eng')
#
#
#     langusage2 = root.find('ead:archdesc/ead:did/ead:langmaterial/ead:language',ns)
#     # print(langusage2)
#     if langusage2 is not None:
#         langusage2.attrib.pop('scriptcode', None)
#
#     #remove all id attrib
#
#     for x in root.iter('*'):
#         name=x.get('id')
#         if name is not None:
#             x.attrib.pop('id', None)
#
#     for el in root.iter('*'):
#         fack=el.attrib
#         for x in fack:
#             attrText = fack[x]
#             if attrText == '5441':
#                 fack[x] = attrText.replace('5441','544')
#             if attrText == '544$1':
#                 fack[x] = attrText.replace('544$1','544')
#
#     #add random ids to containers
#     alldid = root.findall('.//ead:did',ns)
#     for did in alldid:
#         for elem in did.findall('./ead:container[1]',ns):
#             randomID = uuid.uuid4()
#             elem.set('id',str(randomID))
#             newID=elem.get('id')
#             for thing in did.findall('./ead:container',ns):
#                 if thing.get('id') == None:
#                     thing.set('parent',newID)
#
#     return root



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
