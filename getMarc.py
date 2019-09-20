#used for ebook analysis

import requests, json, csv, sys
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import xmltodict
from jsonpath_rw import jsonpath, parse, Fields, Slice
import demjson
import pandas as pd


key = ''
secret = ''

#https://libraries.colorado.edu:443/iii/sierra-api/v5/bibs/10252291/marc

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

with open(sys.argv[1],'rU') as csvFile, open('bibs.csv','w') as outfile:

    # writer = csv.DictWriter(outcsv, fieldnames = ["filename", "original_term", "fast_term", "fast_id", "score"])
    # writer.writeheader()
    reader = csv.DictReader(csvFile)
    # headers={"Content-Type":  "application/json"}

    s = requests.Session()
    resp = s.post('https://libraries.colorado.edu:443/iii/sierra-api/v5/token', auth=(key, secret))
    resp.raise_for_status()
    # print(resp)
    bearer_token = resp.json()['access_token']
    # print(bearer_token)
    # get auth token out of the response
    s.headers["Authorization"] = "Bearer {}".format(bearer_token)
    # print(s.headers)
    # print(s.headers)
    # s.get( # now that is in the session headers - so transparently on all other requests made with this session object
    bibData = {}
    fieldnames = ['id','url','query','totalEvents','uniqueEvents','language','title','author','materialType','publishYear','country','f240a']
    w = csv.DictWriter(outfile, fieldnames, extrasaction='ignore')
    w.writeheader()

#http://libraries.colorado.edu/record=b9103484~S3

#get /v5/bibs/{id}/marc



    for row in reader:
        # print(row)
        # print(row['PermaLink'])

        bib = row['PermaLink'].replace('http://libraries.colorado.edu/record=b','')
        bib = bib[:-3]
        # print(bib)
        # url='https://libraries.colorado.edu:443/iii/sierra-api/v5/bibs/'+bib
        # url ='https://libraries.colorado.edu:443/iii/sierra-api/v5/bibs/9643827'
        url = 'https://libraries.colorado.edu:443/iii/sierra-api/v5/bibs/'+bib+'/marc'
        r = s.get(url, headers={'Accept':'application/marc-in-json'})
        # r = s.get(url, headers={'Accept':'application/marc-xml'})


        if r.status_code == 404:
            pass

        tags =['110','111','130','240','247','780','781','785','260','264','255','257','650','651','652','653','690','691',
        '310','315','321','336','338','337','338','342','343','306','344','346','347','350','352','362','380','381','382','383','384','655','440','490',
        '800','810','811','830','502','504','505','506','508','511','520','521','522','525','533','538','539','541','546','550','555','561','583','586',
        '588','765','767','770','772','773','775','776','777','787','700','710','711','210','246','730','740','793','510','020','022','028','072','536',
        '910','001','019','086','050','856','857','859']
        # rjson=r.json()
        json_data = json.loads(r.text)
        thing=json.dumps(json_data)
        # print(thing)
        # with open("fucj.json", 'r') as f:
        #     first_line = f.readline()
        #     rjson = json.loads(first_line)
        #
        #     print(type(rjson))
        #     print(rjson.keys())
        #
        # if 'fields' not in rjson:
        #     raise Exception()
        if 'fields' in json_data:
            for i, datafield in enumerate(json_data['fields']):
                for marcTag in datafield:
                    if marcTag in tags:
                    # print(inner_key)
                        if 'subfields' not in datafield[marcTag]:
                            pass
                            # "fields.{}.{} - No subfields!".format(
                            # i, marcTag
                            # ))
                        else:
                            for code in datafield[marcTag]['subfields']:

                                for x in code:
                                    # print(x)
                                    # print(code[x])
                                    newCode = marcTag+x
                                    # print(newCode+':'+code[x])
                                    # bibData[marcTag+x] = code[x]

                                # print(code)
                        # print(marcTag,i)
                        # print(
                        # "fields.{}.{} - {}".format(
                        # i, marcTag, datafield[marcTag]['subfields']
                        # ))


                    # for x in datafield[inner_key]['subfields']:
                    #     for whatever_code in x:
                    #         print(x + x[whatever_code])

        # json_data = demjson.decode(r.text)
        # print(json_data)
        # # marc = ['110','111','130','240']
        #
        # if 'fields' in json_data:
        #     for field_key in json_data['fields']:
        #         data_field = json_data['fields'][field_key]
        #         if 'subfields' in data_field:
        #             print(datafield['subfields'])
        #     for datafield in rjson['fields'][0]['subfields']:
        #         print(datafield)

                # for x in datafield:
                #     print(x['subfields'])
                # subfields = datafield.get('subfields')
                # if subfields is not None:
                #     print(subfields['a'])



            # for subfield in record['subfields']:
            #     for key in subfield:
            #         colname = 'subfield_'+key
            #         if colname not in fieldnames:
            #             fieldnames.append(colname)
            #             row[colname] = subfield[key]




        # tree = ET.fromstring(r.text)
        # for x in tree:
        #     print(x)
        # root = tree.getroot()

        # bibData['id'] = bib
        # bibData['url'] = row['PermaLink']
        # bibData['query'] = row['Search URL']
        # bibData['totalEvents'] = row['Total Events']
        # bibData['uniqueEvents'] = row['Unique Events']


        # print(rjson)
        # if rjson['datafield']['tag'] == '110':
        #     print('ok')
        # if 'lang' in rjson:
        #     bibData['language'] = rjson['lang']['name']
        # if 'title' in rjson:
        #     bibData['title'] = rjson['title']
        # if 'author' in rjson:
        #     bibData['author'] = rjson['author']
        # if 'materialType' in rjson:
        #     bibData['materialType'] = rjson['materialType']['value']
        # if 'publishYear' in rjson:
        #     bibData['publishYear'] = rjson['publishYear']
        # if 'country' in rjson:
        #     bibData['country'] = rjson['country']['name']
        # w.writerow(bibData)
