import sys, re, uuid
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import copy, time, datetime
import datetime, requests, json
from fuzzywuzzy import fuzz, process

#this script takes a shapefile and transforms it into a MODS record
#syntax python scriptName nameOfShapefile


def set_if_present(root, xpath, doc, key_to_set):
    """
    Note that this mutates doc, and returns a bool.

    True if it added anything
    False otherwise

    These could be useful for debugging/stats generation
    """
    node_in_tree = root.find(xpath)
    if node_in_tree is not None and node_in_tree.text is not None:
        doc[key_to_set] = node_in_tree.text
        return True

    return False

def get_fast_uri(doc):
    # print(doc)
    jsonDocs = {}
    for term in doc['topics']:
        # print(subject)

        term= term.lower()
        url='http://fast.oclc.org/searchfast/fastsuggest?query='+term+'&queryIndex=suggestall&queryReturn=suggestall,idroot,auth,tag,type,raw,breaker,indicator&suggest=autoSubject&rows=20'

        r = requests.get(url)
        r.raise_for_status()
        rjson = r.json()
        # print(r.text)
        jsonDocs = rjson['response']['docs']

        maxScore = 0.0
        fastValues = None

        # scoreDict = {}
        for x in jsonDocs:
            suggest = x['suggestall'][0]
            suggestLower = x['suggestall'][0].lower()
            fastID = x['idroot']

            score=fuzz.token_sort_ratio(term,suggestLower)
            if score > 80 and score > maxScore:
                maxScore = score
                fastValues = fastID, suggest
                print(maxScore,fastValues)
        #     scoreDict[score] = fastID, suggest
        #
        # ppp = scoreDict[max(scoreDict.keys())] if max(scoreDict.keys()) > 80 else None
        # print(ppp)
        # if scoreDict.keys():
        #     maxKey = max(k for k, v in scoreDict.items())



def getGeoMetadata(infile_path):
    tree=ET.parse(infile_path)
    root=tree.getroot()
    doc = {}
    # print(title)

    doc['filename'] = infile_path
    set_if_present(root, 'idinfo/citation/citeinfo/title', doc, 'title')
    set_if_present(root, 'idinfo/native', doc, 'software')
    set_if_present(root, 'idinfo/citation/citeinfo/pubdate', doc, 'issueDate')
    set_if_present(root, 'idinfo/citation/citeinfo/onlink', doc, 'source')
    set_if_present(root, 'idinfo/citation/citeinfo/origin', doc, 'publisher')
    set_if_present(root, 'dataIdInfo/idCredit', doc, 'creator')
    set_if_present(root, 'idinfo/descript/abstract', doc, 'abstract')


    abstract_node = root.find('idinfo/descript/abstract')
    purpose_node = root.find('idinfo/descript/purpose')
    suppl_node = root.find('idinfo/descript/supplinf')
    enttyped_node = root.find('eainfo/detailed/enttyp/enttypd')
    # This list comprehension sorts out the None elements and crams together the .text strings
    constructed_abstract = "".join(
        [x.text for x in [abstract_node, purpose_node, suppl_node, enttyped_node] if x is not None]
    )
    doc['abstract'] = constructed_abstract

    #fix this
    westbc = root.find('idinfo/spdom/bounding/westbc')
    eastbc = root.find('idinfo/spdom/bounding/southbc')
    northbc = root.find('idinfo/spdom/bounding/eastbc')
    southbc = root.find('idinfo/spdom/bounding/northbc')
    coordinates = "".join(
        [x.text for x in [westbc, eastbc, northbc, southbc] if x is not None]
    )
    # coordinates = 'W'+westbc+','+'W'+eastbc+','+'N'+northbc+','+'N'+southbc
    doc['coordinates'] = coordinates
    #

    doc['topics'] =[]
    keywords = root.findall('idinfo/keywords/theme/themekey')
    if len(keywords) > 0:
        for x in keywords:
            key = x.text
            doc['topics'].append(key)

    doc['places'] = []
    places = root.findall('idinfo/keywords/place/placekey')
    if len(places) > 0:
        for x in places:
            key = x.text
            doc['places'].append(key)
            # print(doc['places'])

    set_if_present(root, 'distinfo/distrib/cntinfo/cntaddr/city', doc, 'city')
    set_if_present(root, 'metainfo/metc/cntinfo/cntaddr/state', doc, 'state')





    searchkeys = root.findall('dataIdInfo/searchKeys/keyword')
    for x in searchkeys:
        key = x.text
        doc['topics'].append(key)

    uses = root.find('idinfo/useconst').text
    doc['note'] = uses
    # for x,y in doc.items():
    #     print(x,y)
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

    # fastSubject = get_fast_uri(doc)
    # print(fastSubject)
    # def add(x, y):
    # answer = x+y
    # return answer
    #
    # def main():
    #     foo = 1
    #     bar = 2
    #     baz = add(foo, bar)
    #     print(baz)

    creator = SubElement(root, 'mods:name')
    creatorTerm = SubElement(creator, 'mods:namePart')
    try:
        creatorTerm.text = doc['creator']
    except KeyError:
        pass

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
    try:
        dateIssued.text = doc['issueDate']
    except KeyError:
        pass


    placeCreated = SubElement(originInfo, 'mods:place')
    placeTerm = SubElement(placeCreated, 'mods:placeTerm')
    try:
        placeTerm.text = doc['state']+'--'+doc['city']
    except KeyError:
        pass
    try:
        placeTerm.text = doc['state']
    except KeyError:
        pass

    #
    pub = SubElement(originInfo, 'mods:publisher')
    pub.text = doc['publisher']
    language = SubElement(root, 'mods:language')
    languageTerm = SubElement(language,'mods:languageTerm')
    languageTerm.set('type','code')
    languageTerm.set('authority', 'iso639-2b')
    languageTerm.text= 'eng'

    jsonDocs={}
    get_fast_uri(doc)
    # for term in doc['topics']:
    #     # print(subject)
    #
    #     term= term.lower()
    #     url='http://fast.oclc.org/searchfast/fastsuggest?query='+term+'&queryIndex=suggestall&queryReturn=suggestall,idroot,auth,tag,type,raw,breaker,indicator&suggest=autoSubject&rows=20'
    #
    #     r = requests.get(url)
    #     r.raise_for_status()
    #     rjson = r.json()
    #     # print(r.text)
    #     jsonDocs = rjson['response']['docs']
    #
    #
    #
    #     # print(docs)
    #     scoreDict = {}
    #     for x in jsonDocs:
    #         suggest = x['suggestall'][0]
    #         suggestLower = x['suggestall'][0].lower()
    #         fastID = x['idroot']
    #
    #         score=fuzz.token_sort_ratio(term,suggestLower)
    #         scoreDict[score] = fastID, suggest
    #     if scoreDict.keys():
    #         maxKey = max(k for k, v in scoreDict.items())



            # if scoreDict.keys() and max(scoreDict.keys()) > 80:
            #
            #     subject = SubElement(root,'mods:subject')
            #     topic = SubElement(subject, 'mods:topic')
            #     subject.set('authority', 'fast')
            #     # topic.text = x['suggestall'][0]
            #     topic.text = suggest
            #     newFast = fastID.replace('fst','')
            #     subject.set('valueURI','http://id.worldcat.org/fast/'+newFast)






        # data = [(1, dog), (2, cat), (2, mouse), (3, horse)]
        #
        # scoreDict = {}
        # for x in data:
        #     if not scoreDict.get(x[0]):
        #         scoreDict[x[0]] = []
        #     scoreDict[x[0]].append(x[1])
        #
        #  for x in scoreDict:
        #     print("Key: " + str(x))
        #     print("Value: " + str(scoreDict[x]))
    # for place in doc['places']:
    #
    #     # placeTerm.text = place
    #     lowerPlace = place.lower()
    #     url='http://fast.oclc.org/searchfast/fastsuggest?query='+place+'&queryIndex=suggest51&queryReturn=suggestall,idroot,auth,tag,type,raw,breaker,indicator&suggest=autoSubject&rows=10'
    #
    #     r = requests.get(url)
    #     r.raise_for_status()
    #     # print(r.text)
    #     rjson = r.json()
    #
    #     jsonDocs = rjson['response']['docs']
    #     # print(docs)
    #
    #     scoreDict={}
    #     for x in jsonDocs:
    #         suggest = x['suggestall'][0]
    #         suggestLower = x['suggestall'][0].lower()
    #         fastID = x['idroot']
    #
    #         score=fuzz.token_sort_ratio(lowerPlace,suggestLower)
    #         scoreDict[score] = fastID, suggest
    #     # print(scoreDict.keys())
    #     if scoreDict.keys() and scoreDict[max(scoreDict.keys())] > 80:
    #         print(scoreDict)

        # print(scoreDict[max(scoreDict.keys())])
        # if max(scoreDict) > 80:
        #     print(scoreDict)
        #     subject = SubElement(root,'mods:subject')
        #     subject.set('authority', 'fast')
        #     subject.set('valueURI','http://id.worldcat.org/fast/'+newFast)
        #     placeTerm = SubElement(subject, 'mods:geographic')
        #     placeTerm.text = x['suggestall'][0]
        #     newFast = fastID.replace('fst','')
        # else:
        #     pass
            # if score > 80:
            #     subject = SubElement(root,'mods:subject')
            #     subject.set('authority', 'fast')
            #     subject.set('valueURI','http://id.worldcat.org/fast/'+newFast)
            #     placeTerm = SubElement(subject, 'mods:geographic')
            #     placeTerm.text = x['suggestall'][0]
            #     newFast = fastID.replace('fst','')

            # else:
            #     subject = SubElement(root,'mods:subject')
            #     placeTerm = SubElement(subject, 'mods:geographic')
            #     placeTerm.text = place


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
    try:
        digNote.text = doc['software']
    except KeyError:
        pass

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
