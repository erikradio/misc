import sys, re, uuid
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import copy, time, datetime
import datetime, requests, json
from fuzzywuzzy import fuzz, process

def getGeoMetadata(infile_path):
    tree=ET.parse(infile_path)
    root=tree.getroot()
    doc = {}
    # print(title)
    title = root.find('idinfo/citation/citeinfo/title').text
    # print(title)
    doc['filename'] = infile_path
    doc['title'] = title
    software = root.find('idinfo/native').text
    doc['software'] = software
    issueDate = root.find('idinfo/citation/citeinfo/pubdate').text
    doc['issueDate'] = issueDate
    source = root.find('idinfo/citation/citeinfo/onlink').text
    doc['source'] = source
    publisher = root.find('idinfo/citation/citeinfo/origin').text
    doc['publisher'] = publisher
    creator = root.find('dataIdInfo/idCredit').text
    doc['creator'] = creator
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

    cityCreated = root.find('distinfo/distrib/cntinfo/cntaddr/city').text
    stateCreated = root.find('metainfo/metc/cntinfo/cntaddr/state').text
    if len(cityCreated) > 0:
        placeCreated = stateCreated+'--'+cityCreated
        doc['placeCreated'] = placeCreated
    else:
        doc['placeCreated'] = stateCreated


    searchkeys = root.findall('dataIdInfo/searchKeys/keyword')
    for x in searchkeys:
        key = x.text
        doc['topics'].append(key)

    uses = root.find('idinfo/useconst').text
    doc['note'] = uses
    return doc

def makeMods(doc):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')

    root = Element('mods:mods')

    root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    root.set('xmlns:mods', 'http://www.loc.gov/mods/v3')
    root.set('xmlns:xlink','http://www.w3.org/1999/xlink')
    root.set('xsi:schemaLocation',
             'http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/mods-3-7.xsd')



    titleInfo = SubElement(root, 'mods:titleInfo')
    title = SubElement(titleInfo, 'mods:title')
    title.text = doc['title']

    pub = SubElement(root, 'mods:name')
    pubTerm = SubElement(pub, 'mods:namePart')
    pubTerm.text = doc['publisher']
    pubRole=SubElement(pub,'mods:role')
    pubRoleTerm = SubElement(pubRole,'mods:roleTerm')
    pubRoleTerm.set('type','text')
    pubRoleTerm.text = 'publisher'
    ##################this doesnt work very well!
    # publisher = doc['publisher']
    # url='http://fast.oclc.org/searchfast/fastsuggest?query='+publisher+'&queryIndex=suggest10&queryReturn=suggestall,idroot,auth&suggest=autoSubject&rows=20'
    #
    # r = requests.get(url)
    # res = json.loads(r.text)
    # jsonDocs=res['response']['docs']
    # for x in jsonDocs:
    #     suggestLower = x['suggestall'][0].lower()
    #     fastID = x['idroot']
    #
    #     score=fuzz.token_sort_ratio(publisher,suggestLower)
    #     if score > 80:
    #         pub.set('authority', 'fast')
    #         pubTerm.text = x['suggestall'][0]
    #         newFast = fastID.replace('fst','')
    #         pub.set('authorityURI','http://id.worldcat.org/fast/'+newFast)




    creator = SubElement(root, 'mods:name')
    creatorTerm = SubElement(creator, 'mods:namePart')
    creatorTerm.text = doc['creator']
    creatorRole=SubElement(creator,'mods:role')
    creatorRoleTerm = SubElement(creatorRole,'mods:roleTerm')
    creatorRoleTerm.set('type','text')
    creatorRoleTerm.text = 'creator'

    type1 = SubElement(root, 'mods:typeOfResource')
    type1.text = 'cartographic'
    type2 = SubElement(root, 'mods:typeOfResource')
    type2.text = 'software, multimedia'
    access = SubElement(root,'mods:accessCondition')

    originInfo = SubElement(root, 'mods:originInfo')

    dateCreated = SubElement(originInfo, 'mods:dateCreated')
    dateCreated.set('encoding', 'w3cdtf')
    dateIssued = SubElement(originInfo,'mods:dateIssued')
    dateIssued.set('encoding', 'w3cdtf')
    dateIssued.text = doc['issueDate']
    #
    #
    placeCreated = SubElement(originInfo, 'mods:place')

    placeTerm = SubElement(placeCreated, 'mods:placeTerm')
    placeTerm.text = doc['placeCreated']

    #
    pub = SubElement(originInfo, 'mods:publisher')
    pub.text = doc['publisher']
    language = SubElement(root, 'mods:language')
    languageTerm = SubElement(language,'mods:languageTerm')
    languageTerm.set('type','code')
    languageTerm.set('authority', 'iso639-2b')
    languageTerm.text= 'eng'
    #
    for term in doc['topics']:
        # print(subject)
        subject = SubElement(root,'mods:subject')
        topic = SubElement(subject, 'mods:topic')
        topic.text = term
        term= term.lower()
        url='http://fast.oclc.org/searchfast/fastsuggest?query='+term+'&queryIndex=suggestall&queryReturn=suggestall,idroot,auth,tag,type,raw,breaker,indicator&suggest=autoSubject&rows=20'

        r = requests.get(url)
        res = json.loads(r.text)
        jsonDocs=res['response']['docs']
        # print(docs)
        for x in jsonDocs:
            suggestLower = x['suggestall'][0].lower()
            fastID = x['idroot']

            score=fuzz.token_sort_ratio(term,suggestLower)
            if score > 80:
                subject.set('authority', 'fast')
                topic.text = x['suggestall'][0]
                newFast = fastID.replace('fst','')
                subject.set('authorityURI','http://id.worldcat.org/fast/'+newFast)


    for place in doc['places']:
        subject = SubElement(root,'mods:subject')
        placeTerm = SubElement(subject, 'mods:geographic')
        # placeTerm.text = place
        place = place.lower()
        url='http://fast.oclc.org/searchfast/fastsuggest?query='+place+'&queryIndex=suggest51&queryReturn=suggestall,idroot,auth,tag,type,raw,breaker,indicator&suggest=autoSubject&rows=20'

        r = requests.get(url)
        res = json.loads(r.text)
        jsonDocs=res['response']['docs']
        # print(docs)
        for x in jsonDocs:
            suggestLower = x['suggestall'][0].lower()
            fastID = x['idroot']

            score=fuzz.token_sort_ratio(place,suggestLower)
            if score > 80:
                subject.set('authority', 'fast')
                placeTerm.text = x['suggestall'][0]
                newFast = fastID.replace('fst','')
                subject.set('authorityURI','http://id.worldcat.org/fast/'+newFast)


    latlong = SubElement(root, 'mods:subject')
    carto = SubElement(latlong,'mods:cartographics')
    cartoCoord = SubElement(carto, 'mods:coordinates')
    cartoCoord.text = doc['coordinates']



    # info about the nature of the resource
    physDesc = SubElement(root, 'mods:physicalDescription')

    digOr = SubElement(physDesc, 'mods:digitalOrigin')
    digOr.text = 'born digital'
    form = SubElement(physDesc, 'mods:form')
    form.set('authority', 'LCGFT')
    form.set('authorityURI','http://id.loc.gov/authorities/genreForms/gf2011026721')
    form.text = 'Vector data'
    digNote = SubElement(physDesc,'mods:note')
    digNote.text = doc['software']

    identifier = SubElement(root,'mods:identifier')
    identifier.set('type','local')
    identifier.text = doc['filename']
    #
    interMed = SubElement(physDesc, 'mods:internetMediaType')
    interMed.text = 'application/octet-stream'

    abstract = SubElement(root, 'mods:abstract')
    abstract.text = doc['abstract']

    note = SubElement(root, 'mods:note')
    note.text = doc['note']
    accessCond = SubElement(root, 'mods:accessCondition')

    location = SubElement(root, 'mods:location')
    url = SubElement(location, 'mods:url')
    url.set('access', 'object in context')


    relatedItem = SubElement(root, 'mods:relatedItem')
    relatedItem.set('type', 'otherVersion')
    source = doc['source']
    relatedItem.set('xlink:href', source)
    relatedTitleInfo = SubElement(relatedItem,'mods:titleInfo')
    relatedTitle = SubElement(relatedTitleInfo,'mods:title')
    relatedTitle.text = doc['title']



    recordInfo = SubElement(root,'mods:recordInfo')
    recordCreationDate = SubElement(recordInfo,'mods:recordCreationDate')
    recordCreationDate.set('encoding','w3cdtf')
    recordCreationDate.text = st
    recordOrigin = SubElement(recordInfo,'mods:recordOrigin')
    recordOrigin.text = 'Record created using source metadata and additional metadata provided by the University of Colorado Boulder Libraries.'
    recordSource = SubElement(recordInfo,'mods:recordContentSource')
    recordSource.text = 'University of Colorado Boulder Libraries'
    tree = ET.ElementTree(root)


    return tree




def main():
    infile_path = sys.argv[1]
    outfile_path = 'mods_'+sys.argv[1]

    doc=getGeoMetadata(infile_path)
    newtree=makeMods(doc)
    newtree.write(outfile_path, encoding="utf8")

if __name__ == '__main__':
    main()
