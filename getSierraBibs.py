import requests, json, csv, sys
from fuzzywuzzy import fuzz, process
from xml.etree.ElementTree import Element, SubElement, Comment, tostring

key = ''
secret = ''

#https://libraries.colorado.edu:443/iii/sierra-api/v5/bibs/10252291/marc

with open(sys.argv[1],'rU') as csvFile, open('bibs.csv','w') as outfile:

    # writer = csv.DictWriter(outcsv, fieldnames = ["filename", "original_term", "fast_term", "fast_id", "score"])
    # writer.writeheader()
    reader = csv.DictReader(csvFile)
    headers={"Content-Type":  "application/json"}

    s = requests.Session()
    resp = s.post( 'https://libraries.colorado.edu:443/iii/sierra-api/v5/token', auth=(key, secret))
    resp.raise_for_status()
    bearer_token = resp.json()['access_token']
    # print(bearer_token)
    # get auth token out of the response
    s.headers["Authorization"] = "Bearer {}".format(bearer_token)
    # s.get( # now that is in the session headers - so transparently on all other requests made with this session object
    bibData = {}
    fieldnames = ['id','language','title','author','materialType','publishYear','country']
    w = csv.DictWriter(outfile, fieldnames)
    w.writeheader()

    # {'id': '4138916', 'updatedDate': '2014-11-25T17:13:37Z', 'createdDate': '2007-01-19T23:21:00Z', 'deleted': False, 'suppressed': False, 'lang': {'code': 'eng', 'name': 'English'}, 'title': 'Insurance maps of Cripple Creek, Teller Co., Colorado', 'author': 'Sanborn Map Company', 'materialType': {'code': 'e  ', 'value': 'Maps'}, 'bibLevel': {'code': 'o', 'value': 'ORIGINAL'}, 'publishYear': 1909, 'catalogDate': '2007-01-19', 'country': {'code': 'nyu', 'name': 'New York'}}
    for row in reader:
        # print(row)
        # print(row['PermaLink'])

        bib = row['PermaLink'].replace('http://libraries.colorado.edu/record=b','')
        bib = bib[:-3]
        # print(bib)
        url='https://libraries.colorado.edu:443/iii/sierra-api/v5/bibs/'+bib
        r = s.get(url)
        rjson = r.json()

        bibData['id'] = bib
        # bibData['createdDate'] = rjson['createdDate']
        if 'lang' in rjson:
            bibData['language'] = rjson['lang']['name']
        if 'title' in rjson:
            bibData['title'] = rjson['title']
        if 'author' in rjson:
            bibData['author'] = rjson['author']
        if 'materialType' in rjson:
            bibData['materialType'] = rjson['materialType']['value']
        if 'publishYear' in rjson:
            bibData['publishYear'] = rjson['publishYear']
        if 'country' in rjson:
            bibData['country'] = rjson['country']['name']
        w.writerow(bibData)
