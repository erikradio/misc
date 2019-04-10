import sys, re, uuid
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import copy
from datetime import datetime

def getGeoMetadata(infile_path):
    tree=ET.parse(infile_path)
    root=tree.getroot()
    doc = {}
    # print(title)
    title = root.find('idinfo/citation/citeinfo/title').text
    # print(title)
    doc['title'] = title

    issueDate = root.find('idinfo/citation/citeinfo/pubdate').text
    doc['issueDate'] = issueDate
    source = root.find('idinfo/citation/citeinfo/onlink').text
    doc['source'] = source
    publisher = root.find('idinfo/citation/citeinfo/origin').text
    doc['publisher'] = publisher
    abstract = root.find('idinfo/descript/abstract').text
    purpose = root.find('idinfo/descript/purpose').text
    suppl = root.find('idinfo/descript/supplinf').text
    enttypepd = root.find('eainfo/detailed/enttyp/enttypd').text
    doc['abstract'] = abstract+purpose+suppl+enttypepd

    westbc = root.find('idinfo/spdom/bounding/westbc').text.strip('-')
    eastbc = root.find('idinfo/spdom/bounding/southbc').text.strip('-')
    northbc = root.find('idinfo/spdom/bounding/eastbc').text.strip('-')
    southbc = root.find('idinfo/spdom/bounding/northbc').text.strip('-')
    coordinates = 'W'+westbc+','+'W'+eastbc+','+'N'+northbc+','+'N'+southbc
    doc['coordinates'] = coordinates

    doc['topics'] =[]
    keywords = root.findall('idinfo/keywords/theme/themekey')
    for x in keywords:
        key = x.text
        doc['topics'].append(key)
    doc['places'] = []
    places = root.findall('idinfo/keywords/place/placekey')
    for x in places:
        key = x.text
        doc['places'].append(key)

    searchkeys = root.findall('dataIdInfo/searchKeys/keyword')
    for x in searchkeys:
        key = x.text
        doc['topics'].append(key)

    uses = root.find('idinfo/useconst').text
    doc['note'] = uses
    return doc

def makeMods(doc):

    for x in doc:
        print(x)
# newnewroot = Element('mods:mods')
#
# newnewroot.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
# newnewroot.set('xmlns:mods', 'http://www.loc.gov/mods/v3')
# newnewroot.set('xmlns:xlink','http://www.w3.org/1999/xlink')
# newnewroot.set('xsi:schemaLocation',
#          'http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-6.xsd')
# newtree = ET.ElementTree(newroot)
# # record = SubElement(newroot, 'mods:mods')
# # record.set('xsi:schemaLocation',
# #            'http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-6.xsd')
# # inserts filename as local identifier
# identifier = SubElement(newroot, 'mods:identifier')
# identifier.set('type', 'local')
# id = row['identifier']
# identifier.text = row['identifier']
#
# titleInfo = SubElement(newroot, 'mods:titleInfo')
# title = SubElement(titleInfo, 'mods:title')
# title.text = row['title']
#
# partNo = SubElement(titleInfo, 'mods:partNumber')
# partNo.text = row['part']
# typeImage = SubElement(newroot, 'mods:typeOfResource')
# typeImage.text = row['typeOfResource']
#
# originInfo = SubElement(newroot, 'mods:originInfo')
#         if len(row['dateCreated']) > 0:
#             dateCreated = SubElement(originInfo, 'mods:dateCreated')
#             dateCreated.set('encoding', 'w3cdtf')
#             dateCreated.text = row['dateCreated']
#
#         placeCreated = SubElement(originInfo, 'mods:place')
#         placeCreated.set('supplied', 'yes')
#         placeTerm = SubElement(placeCreated, 'mods:placeTerm')
#         placeTerm.set('authorityURI', 'http://id.worldcat.org/fast')
#         placeTerm.set('valueURI', 'http://id.worldcat.org/fast/1205454')
#         placeTerm.text = row['placeCreated']
#
#         pub = SubElement(originInfo, 'mods:publisher')
#         pub.text = row['publisher']
#
#
#         langrow=row['language'].split('|')
#         for x in langrow:
#             language = SubElement(newroot, 'mods:language')
#             languageTerm = SubElement(language,'mods:languageTerm')
#             languageTerm.set('type','text')
#             languageTerm.text=x
#         # if '|' in row['Language']:
#         #     posh = row['Language'].split('|')
#         #
#         #     for x in posh:
#         #         language.text=str(x)
#         #     # print(language)
#         #     # language.text = language
#         # else:
#         #     language.text = row['Language']
#
#         namerow = row['creatorName'].split('|')
#
#
#
#         for x in namerow:
#
#             name = SubElement(newroot, 'mods:name')
#             name.set('type', 'personal')
#             namePart = SubElement(name, 'mods:namePart')
#             if ';' in x:
#                 role = SubElement(name, 'mods:role')
#                 # roleTermcode = SubElement(role, 'mods:roleTerm')
#                 # roleTermcode.set('type', 'code')
#
#                 roleTermtext = SubElement(role, 'mods:roleTerm')
#                 roleTermtext.set('type', 'text')
#                 y = x.split(';')
#                 namePart.text = y[0]
#                 roleTermtext.text = y[1]
#
#             else:
#                 namePart.text = x
#
#
#         # info about the nature of the resource. not from the spreadsheet
#         physDesc = SubElement(newroot, 'mods:physicalDescription')
#         if len(row['digitalOrigin']) > 0:
#             digOr = SubElement(physDesc, 'mods:digitalOrigin')
#             digOr.text = row['digitalOrigin']
#         form = SubElement(physDesc, 'mods:form')
#         form.set('type', 'material')
#         form.text = row['form']
#
#         identifier = SubElement(newroot,'mods:identifier')
#         identifier.set('type','local')
#         identifier.text = row['identifier']
#
#         interMed = SubElement(physDesc, 'mods:internetMediaType')
#         interMed.text = 'audio/wav'
#         #
#         abstract = SubElement(newroot, 'mods:abstract')
#         abstract.text = row['abstract']
#
#         genre = SubElement(newroot, 'mods:genre')
#         genre.set('authorityURI', 'http://id.loc.gov')
#         genre.set(
#             'valueURI', 'http://id.loc.gov/authorities/genreForms/gf2011026431.html')
#         genre.text = row['genre']
#         accessCond = SubElement(newroot, 'mods:accessCondition')
#         accessCond.set('type', 'use and reproduction')
#         # accessCond.set('xlink:href','http://rightsstatements.org/page/UND/1.0/?language=en')
#         accessCond.text = 'The copyright and related rights status of this Item has been reviewed by the organization that has made the Item available, but the organization was unable to make a conclusive determination as to the copyright status of the Item. Please refer to the organization that has made the Item available for more information. You are free to use this Item in any way that is permitted by the copyright and related rights legislation that applies to your use.'
#         #
#
#         location = SubElement(newroot, 'mods:location')
#         physLoc = SubElement(location, 'mods:physicalLocation')
#         physLoc.set('authorityURI', 'http://id.worldcat.org/fast')
#         physLoc.set('valueURI', 'http://id.worldcat.org/fast/1567592')
#         shelfLocator = SubElement(location, 'mods:shelfLocator')
#         shelfLocator.text = row['callNumber'] + ', ' + row['shelfLocator']
#         shelfLocator = SubElement(location, 'mods:shelfLocator')
#         shelfLocator.text = row['callNumberID']
#         physLoc.text = 'University of Arizona. Library. Special Collections.'
#         # typeOfResource = SubElement(newroot, 'mods:typeOfResource')
#         # typeOfResource.text = row['TypeOfResource']
#         # related item was used for the host parent of the plate, e.g. the
#         # monographic volume
#         relatedItem = SubElement(newroot, 'mods:relatedItem')
#         relatedItem.set('type', 'host')
#         relatedTitleInfo = SubElement(relatedItem,'mods:titleInfo')
#         relatedTitle = SubElement(relatedTitleInfo,'mods:title')
#
#         relatedTitle.text = row['relatedItem']
#
#         recordInfo = SubElement(newroot,'mods:recordInfo')
#         recordCreationDate = SubElement(recordInfo,'mods:recordCreationDate')
#         recordCreationDate.set('encoding','w3cdtf')
#         recordCreationDate.text = st
#         recordOrigin = SubElement(recordInfo,'mods:recordOrigin')
#         recordOrigin.text = 'Manually created by Trent Purdy. Generated into xml using a python script by Erik Radio.'
#         recordSource = SubElement(recordInfo,'mods:recordContentSource')
#         recordSource.text = 'University of Colorado Boulder Libraries'
#         tree.write(identifier.text + '.xml', xml_declaration=True, encoding="UTF-8")

def main():
    infile_path = sys.argv[1]
    outfile_path = 'mods_'+sys.argv[1]

    doc=getGeoMetadata(infile_path)
    makeMods(doc)
if __name__ == '__main__':
    main()
