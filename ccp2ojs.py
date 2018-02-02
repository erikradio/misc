# -- python3 --
import csv, re, sys, time, datetime, xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring


dataFile=sys.argv[1]


ts=time.time()
st=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')

volumesDict={}
with open(dataFile, 'rU') as csvfile:

    reader = csv.DictReader(csvfile)
    # columnList=next(reader)

    # initialize xml tree
    root = Element('issues')
    tree=ET.ElementTree(root)

    # put all the article data into a list
    articleList=[]
    volumesList={}

    for row in reader:

        articleList.append(row)
        volumesID=row['Volume_ID_Number']
        # volumesTitle=row['Volume']
        volumeDate=row['Date_Published']
        volumesList.update({volumesID:[volumeDate,volumesTitle]})
    # print (volumesList)


    # create the issue level data from the dictionary
    for y in volumesList:
        issue=SubElement(root,'issue')
        issue.set('current','false')
        issue.set('published','true')
        issue.set('identification','title')

        issueTitle=SubElement(issue,'title')
        issueTitle.text=volumesList.get(y)[0]
        issueDate=SubElement(issue,'year')
        issueDate.text=volumesList.get(y)[1]
        # print(issueDate.text)

        accessDate=SubElement(issue,'access_date')
        accessDate.text='2018-01-01'
        section=SubElement(issue,'section')
        sectionTitle=SubElement(section,'title')
        sectionTitle.text='Articles'




        # link up article volume id to dictionary, when they match, extend the issue with the articles
        for x in articleList:

            volID=x['Volume_ID_Number']
            author=x['Author']
            # print(author)
            if volID==y:


#
                article=SubElement(section,'article')
                articleID=SubElement(article,'id')

                articleID.text=x['PDF_Filename']
                articleTitle=SubElement(article,'title')
                articleTitle.text=x['Article_Title']
                articleDate=SubElement(article,'date_published')
                articleDate.text=x['Date_Published']

                galley=SubElement(article,'galley')
                label=SubElement(galley,'label')
                label.text='PDF'
                fileSec=SubElement(galley,'file')
                fileLoc=SubElement(fileSec,'href')
                fileLoc.set('src','http://maps.lib.ku.edu/mapscoll/transfer/chimeres/'+x['PDF_Filename'])
                fileLoc.set('mime_type','application/pdf')

                if len(author)>0:
                    if '||' not in author:
                        if ',' in author:
                            lastName,firstName=author.split(', ')

                            authorPrim=SubElement(article,'author')
                            authorPrim.set('primary_contact','true')

                            authorPLast=SubElement(authorPrim,'lastname')
                            authorPLast.text=lastName

                            auPFirst=SubElement(authorPrim,'firstname')
                            auPFirst.text=firstName
                            email=SubElement(authorPrim,'email')
                            email.text='test@email.arizona.edu'
                        else:
                            authorPrim=SubElement(article,'author')
                            authorPrim.set('primary_contact','true')

                            authorPLast=SubElement(authorPrim,'lastname')
                            authorPLast.text=author
                            email=SubElement(authorPrim,'email')
                            email.text='test@email.arizona.edu'
                    elif '||' in author:
                        names=author.split('||')
                        nameList=list(enumerate(names))

                        for i,x in enumerate(names):

                            if i==0:
                                lastName,firstName=x.split(', ')
                                authorPrim=SubElement(article,'author')
                                authorPrim.set('primary_contact','true')

                                authorPLast=SubElement(authorPrim,'lastname')
                                authorPLast.text=lastName

                                auPFirst=SubElement(authorPrim,'firstname')
                                auPFirst.text=firstName
                                email=SubElement(authorPrim,'email')
                                email.text='test@email.arizona.edu'
                            elif i!=0:


                                lastName,firstName=x.split(', ')

                                authorNotPrim=SubElement(article,'author')
                                authorNotPrim.set('primary_contact','false')
                                auLast=SubElement(authorNotPrim,'lastname')
                                auLast.text=lastName

                                auFirst=SubElement(authorNotPrim,'firstname')
                                auFirst.text=firstName
                                email=SubElement(authorNotPrim,'email')
                                email.text='test@email.arizona.edu'

with open('newCCP_OJS.xml','w') as f:
    tree.write(f, xml_declaration=True,encoding='utf-8')
