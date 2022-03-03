import sys, pdb, rdflib
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import datetime, requests, json
from SPARQLWrapper import SPARQLWrapper, XML, JSON

def get_uri(term):
    # print(doc)
    results = []
    jsonDocs = {}
    term = (str(term))
    # print(term)
    url='http://fast.oclc.org/searchfast/fastsuggest?query='+term+'&queryIndex=suggestall   &queryReturn=suggestall,idroot,auth,tag,type,raw,breaker,indicator&suggest=autoSubject&rows=5'
    # print(term)
    r = requests.get(url)
    r.raise_for_status()
    rjson = r.json()
    # print(r.text)
    jsonDocs = rjson['response']['docs']
    # print(jsonDocs)
    fastValues = None
    if jsonDocs:
        for x in jsonDocs:
            # print(x)
            suggest = x['suggestall'][0]
            auth = x['auth']
            fastID = x['idroot']
            print('original: '+term +' | '+ 'FAST: '+ suggest +' ('+fastID+')')
            user_response = input("Select this FAST heading? [y/n/x]")
            if user_response.lower().startswith("y"):
                fastValues = fastID, suggest
                results.append(fastValues)
                break
            if user_response.lower().startswith("x"):
                fastValues = '',''

                results.append(fastValues)
                break
        if fastValues is None:
            print("No heading has been selected; '" + term +"' will be retained.")
            fastValues = '', term
            results.append(fastValues)
    else:
        print('No matches found for '+ term +'; the original term will be retained')

            # fastValues = '',term
            # results.append(fastValues)


    return results

def get_aat(term):

    # first method
    # s = sparql.Service('http://vocab.getty.edu/sparql', "utf-8", "GET")
    # query = ('select * {?term rdfs:label "' + term +'"@en}')
    # r = sparql.query('http://vocab.getty.edu/sparql', query)
    # for row in r:
    #     # print ('row:', row)
    #     values = sparql.unpack_row(row)
    #     print (values[0], "-", values[1])

#second method (doesnt work)
    # sparql = SPARQLWrapper("http://vocab.getty.edu")
    # sparql.setQuery('select * {?term rdfs:label "' + term +'"@en}')
    #
    # sparql.setReturnFormat(JSON)
    # results = sparql.query().convert()
    # print(results)





#third method - sort of works
    url = 'http://vocab.getty.edu/sparql'
    query = 'select ?term ?termLabel {?term rdfs:label "' + term +'"@en}'
    # print(query)
    r = requests.get(url, params = {'format': 'json', 'query': query})
    data = r.json()

    print(data)
    # results = term




    results=term


    return results

###
# ?x gvp:prefLabelGVP [xl:literalForm ?label]
#
#
#
# http://vocab.getty.edu/sparql.json?query=select+*+%7B%3Fx+luc%3Aterm+%22vincent+van+gogh%22%3Bskos%3AinScheme+ulan%3A%3Bgvp%3AprefLabelGVP%2Fxl%3AliteralForm+%3Fname%3Brdf%3Atype+gvp%3APersonConcept%7D&_implicit=false&implicit=true&_equivalent=false&_form=%2Fsparql

###

def getMetadata(infile_path):
    tree=ET.parse(infile_path)
    root=tree.getroot()
    doc = {}
    ns = {'mods':'http://www.loc.gov/mods/v3'}

#get topical subjects
    for subjects in root.findall('mods:subject',ns):
    #
    #     for topic in subjects.findall('mods:topic',ns):
    #         term = topic.text
    #
    #         if 'valueURI' not in topic.attrib:
    #             for result in get_uri(term):
    #                 if len(result[0]) > 0:
    #                     topic.set('authority', 'fast')
    #                     topic.text = result[1]
    #                     topic.set('valueURI','http://id.worldcat.org/fast/'+result[0])
    #                 else:
    #                     topic.text = result[1]
    #         else:
    #             continue

#get uris for geographic subjects
        # for place in subjects.findall('mods:geographic',ns):
        #     # print(place.text)
        #     placeTerm = place.text
        #     if 'valueURI' not in place.attrib:
        #         for result in get_uri(placeTerm):
        #             if len(result[0]) > 0:
        #                 place.set('authority', 'fast')
        #                 place.text = result[1]
        #                 place.set('valueURI','http://id.worldcat.org/fast/'+result[0])
        #             else:
        #                 place.text = result[1]
        #             # print(place.attrib)
        #
        #     else:
        #         continue

# get uris for subject names
        for name in subjects.findall('mods:name',ns):
            # print(name.attrib)
            for namePart in name.findall('mods:namePart',ns):
                if 'valueURI' not in name.attrib:
                    nameTerm = namePart.text
                    # print(nameTerm)
                    for result in get_uri(nameTerm):
                        if len(result[0]) > 0:
                            name.set('authority', 'fast')

                            name.set('valueURI','http://id.worldcat.org/fast/'+result[0])
                            namePart.text = result[1]
                        if len(result[1]) > 0:
                            namePart.text = result[1]
                        else:
                            continue


            else:
                continue

#get uris for any names not in subjects
    # for name in root.findall('mods:name',ns):
    #     # print(name.text)
    #     for namePart in name.findall('mods:namePart',ns):
    #         if 'valueURI' not in name.attrib:
    #             nameTerm = namePart.text
    #             # print(nameTerm)
    #             for result in get_uri(nameTerm):
    #                 if len(result[0]) > 0:
    #                     name.set('authority', 'fast')
    #
    #                     name.set('valueURI','http://id.worldcat.org/fast/'+result[0])
    #                     namePart.text = result[1]
    #                     # print(result[0])
    #                     # print(name.attrib)
    #
    #     else:
    #         continue

#get uris for place in originInfo
    # for place in root.findall('mods:originInfo/mods:place/mods:placeTerm',ns):
    #
    #     if 'valueURI' not in place.attrib:
    #         placeTerm = place.text.replace('-',' ')
    #
    #         # print(placeTerm)
    #         for result in get_uri(placeTerm):
    #             print(result)
    #             if len(result[0]) > 0:
    #                 place.set('authority', 'fast')
    #                 print(place.attrib)
    #                 place.text = result[1]
    #                 place.set('valueURI','http://id.worldcat.org/fast/'+result[0])
    #             else:
    #                 place.text = result[1]
    #             # print(place.attrib)
    #
    #     else:
    #         continue
    # return root

#get uris for _form
    for form in root.findall('mods:physicalDescription/mods:form',ns):
        # print(form.attrib)

        if 'valueURI' not in form.attrib:
            formTerm = form.text

            # print(formTerm)
            for result in get_aat(formTerm):
                x=1
        #         if len(result[0]) > 0:
        #             place.set('authority', 'fast')
        #             print(place.attrib)
        #             place.text = result[1]
        #             place.set('valueURI','http://id.worldcat.org/fast/'+result[0])
        #         else:
        #             place.text = result[1]
        #         # print(place.attrib)
        #
        # else:
        #     continue
    return root



def main():
    infile_path = sys.argv[1]
    outfile_path = 'mods_test'+sys.argv[1]


    doc=getMetadata(infile_path)
    tree=ET.ElementTree(doc)
    ET.register_namespace('mods',"http://www.loc.gov/mods/v3")

    tree.write('rev'+outfile_path, encoding="utf8")

if __name__ == '__main__':
    main()
