# -- coding: utf-8 --
import sys, re, uuid, csv
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement
import copy, time, datetime
import requests, json
from fuzzywuzzy import fuzz, process
from random import randint


# 2015-10-07. Converts gould_books.csv to MODS. Records are for plates only but book records can be derived or use existing MARC records.
# dict[key][0] etc
# add second date for bird ksrl_sc_gould_ng_1_2_002.tif - 1880:01:01

# xmlData = open(xmlFile, 'w')


TS = time.time()
ST = datetime.datetime.fromtimestamp(TS).strftime('%Y-%m-%d')

# sanborn uri http://id.loc.gov/authorities/names/n80084431


def get_topic_uri(subjects):
    # print(doc)
    results = []
    jsonDocs = {}
    for term in subjects:
        # print(term)

        term= term.lower()
        url='http://fast.oclc.org/searchfast/fastsuggest?query='+term+'&queryIndex=suggestall&queryReturn=suggestall,idroot,auth,tag,type,raw,breaker,indicator&suggest=autoSubject&rows=20'

        r = requests.get(url)
        r.raise_for_status()
        rjson = r.json()
        # print(r.text)
        jsonDocs = rjson['response']['docs']
        maxScore = 0.0
        fastValues = None
        for x in jsonDocs:
            # print(x)
            suggest = x['suggestall'][0]
            suggestLower = x['suggestall'][0].lower()
            fastID = x['idroot']

            score=fuzz.token_sort_ratio(term,suggestLower)
            if score > 80 and score > maxScore:
                maxScore = score
                fastValues = fastID, suggest
                results.append(fastValues)
    # print(results)
    return results


def makeMods():
    with open(sys.argv[1], 'rU', errors='ignore') as csvFile:

        reader = csv.DictReader(csvFile)

        for row in reader:
            # print(row)
            # if row['identifier'] in seen:
            #     continue
            #
            # seen.add(row['identifier'])
            root = Element('mods:modsCollection')
            root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
            root.set('xmlns:mods', 'http://www.loc.gov/mods/v3')
            root.set('xmlns:xlink','http://www.w3.org/1999/xlink')
            root.set('xsi:schemaLocation',
                     'http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-7.xsd')


            record = SubElement(root, 'mods:mods')
            record.set('xsi:schemaLocation',
                       'http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-6.xsd')
            # inserts filename as local identifier
            identifier = SubElement(record, 'mods:identifier')
            identifier.set('type', 'local')
            identifier.text = row['url']

            oclc = row['identifier']
            filename= row['filename'].strip('.tif')
            arkID = SubElement(record, 'mods:identifier')
            arkID.set('type','ark')
            arkID.text = 'https://ark.colorado.edu/ark:47540/'+oclc+'-'+filename
            newFile = 'mods_'+'ark:47540_'+oclc+'-'+filename+'.xml'


            titleInfo = SubElement(record, 'mods:titleInfo')
            title = SubElement(titleInfo, 'mods:title')
            title.text = row['title']

            partNo = SubElement(titleInfo, 'mods:partNumber')
            partNo.text = row['part']
            typeImage = SubElement(record, 'mods:typeOfResource')
            typeImage.text = 'cartographic'

            originInfo = SubElement(record, 'mods:originInfo')
            dateCreated = SubElement(originInfo, 'mods:dateIssued')
            dateCreated.set('encoding', 'w3cdtf')
            dateCreated.text = row['dateIssued']

            placeCreated = SubElement(originInfo, 'mods:place')
            placeCreated.set('supplied', 'yes')
            placeTerm = SubElement(placeCreated, 'mods:placeTerm')
            placeTerm.set('authorityURI', 'http://id.worldcat.org/fast')
            placeTerm.set('valueURI', 'http://id.worldcat.org/fast/1204333')
            placeTerm.text = row['placeCreated']

            pub = SubElement(originInfo, 'mods:publisher')
            pub.text = row['publisher']

            subjects = row['subjectTopic']
            # print(get_topic_uri(subjects))
            # for result in get_topic_uri(subjects):
            #
            #     # print(result)
            #     subject = SubElement(root,'mods:subject')
            #     topic = SubElement(subject, 'mods:topic')
            #     subject.set('authority', 'fast')
            #     topic.text = result[1]
            #     subject.set('valueURI','http://id.worldcat.org/fast/'+result[0])
                # print(topic.text)
            # langrow=row['Language'].split('|')
            # for x in langrow:
            #     language = SubElement(record, 'mods:language')
            #     languageTerm = SubElement(language,'mods:languageTerm')
            #     languageTerm.set('type','text')
            #     languageTerm.text=x
            # if '|' in row['Language']:
            #     posh = row['Language'].split('|')
            #
            #     for x in posh:
            #         language.text=str(x)
            #     # print(language)
            #     # language.text = language
            # else:
            #     language.text = row['Language']

            namerow = row['creator'].split('|')



            for x in namerow:
                name = SubElement(record, 'mods:name')
                name.set('type', 'personal')
                namePart = SubElement(name, 'mods:namePart')
                if ';' in namerow:
                    role = SubElement(name, 'mods:role')
                    # roleTermcode = SubElement(role, 'mods:roleTerm')
                    # roleTermcode.set('type', 'code')

                    roleTermtext = SubElement(role, 'mods:roleTerm')
                    roleTermtext.set('type', 'text')
                    y = x.split(';')
                    namePart.text = y[0]
                else:
                    namePart.text = x


            # info about the nature of the resource. not from the spreadsheet
            note = SubElement(record, 'mods:note')
            note.text = row['note']
            physDesc = SubElement(record, 'mods:physicalDescription')
            if len(row['digitalOrigin']) > 0:
                digOr = SubElement(physDesc, 'mods:digitalOrigin')
                digOr.text = row['digitalOrigin']
            form = SubElement(physDesc, 'mods:form')
            form.set('type', 'material')
            form.set('authorityURI','http://vocab.getty.edu')
            form.set('valueURI', 'http://vocab.getty.edu/page/aat/300418022')
            form.text = 'city maps'


            interMed = SubElement(physDesc, 'mods:internetMediaType')
            interMed.text = 'image/tiff'

            abstract = SubElement(record, 'mods:abstract')
            abstract.text = row['abstract']

            # genre = SubElement(record, 'mods:genre')
            # genre.set('authorityURI', 'http://id.loc.gov')
            # genre.set(
            #     'valueURI', 'http://id.loc.gov/authorities/genreForms/gf2011026431.html')
            # genre.text = 'Oral histories'
            accessCond = SubElement(record, 'mods:accessCondition')
            accessCond.set('type', 'use and reproduction')
            accessCond.set('xlink:href','https://rightsstatements.org/page/NoC-NC/1.0/?language=en')
            accessCond.text = 'You can, without permission, copy, modify, distribute, display, or perform the Item, for non-commercial uses. For any other permissible uses, please review the terms and conditions of the organization that has made the Item available.'
            #

            location = SubElement(record, 'mods:location')
            physLoc = SubElement(location, 'mods:physicalLocation')
            physLoc.set('authorityURI', 'http://id.worldcat.org/fast')
            physLoc.set('valueURI', 'http://id.worldcat.org/fast/538295')
            # shelfLocator = SubElement(location, 'mods:shelfLocator')
            # shelfLocator.text = row['CallNumber'] + ', ' + row['ShelfLocator']
            physLoc.text = row['holdingInst']

            # related item was used for the host parent of the plate, e.g. the
            # monographic volume
            relatedItem = SubElement(record, 'mods:relatedItem')
            relatedItem.set('type', 'host')
            relatedTitleInfo = SubElement(relatedItem,'mods:titleInfo')
            relatedTitle = SubElement(relatedTitleInfo,'mods:title')
            #
            relatedTitle.text = row['relatedTitle']

            recordInfo = SubElement(record,'mods:recordInfo')
            recordCreationDate = SubElement(recordInfo,'mods:recordCreationDate')
            recordCreationDate.set('encoding','w3cdtf')
            recordCreationDate.text = ST
            recordOrigin = SubElement(recordInfo,'mods:recordOrigin')
            recordOrigin.text = 'Metadata provided by the University of Colorado Boulder Libraries.'
            recordSource = SubElement(recordInfo,'mods:recordContentSource')
            recordSource.set('authorityURI', 'http://id.worldcat.org/fast')
            recordSource.set('valueURI', 'http://id.worldcat.org/fast/538295')
            recordSource.text = 'University of Colorado Boulder Libraries'
            recordID = SubElement(recordInfo,'mods:recordIdentifier')
            recordID.text = newFile.strip('.xml')
            # print(newFile)
            tree = ET.ElementTree(root)
            # print(tree, newFile)
            tree.write(newFile, encoding="utf8")


def main():

    makeMods()


if __name__ == '__main__':
    main()
