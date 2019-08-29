import requests, json, csv, sys
from fuzzywuzzy import fuzz, process
from xml.etree.ElementTree import Element, SubElement, Comment, tostring

key = ''
secret = ''

#https://libraries.colorado.edu:443/iii/sierra-api/v5/bibs/10252291/marc

with open(sys.argv[1],'rU') as csvFile, open('sampleJson.json','w') as outfile:

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
    output = []
    for row in reader:
        # print(row)
        # print(row['PermaLink'])

        bib = row['PermaLink'].replace('http://libraries.colorado.edu/record=b','')
        bib = bib[:-3]
        # print(bib)
        url='https://libraries.colorado.edu:443/iii/sierra-api/v5/bibs/'+bib
        r = s.get(url)
        rjson = r.json()
        output.append(rjson)
        print(output)
    # test='http://fast.oclc.org/searchfast/fastsuggest?&query=hog&queryIndex=suggestall&queryReturn=suggestall,idroot,auth,tag,type,raw,breaker,indicator&suggest=autoSubject&rows=10'
    #http://fast.oclc.org/searchfast/fastsuggest?query=dog&queryIndex=suggestall@queryReturn=suggestall,idroot,auth,tag,type,raw,breaker,indicator&suggest=autoSubject&rows=3&callback=testcall
    # terms=['denver']
    # for term in terms:
    #     url='http://fast.oclc.org/searchfast/fastsuggest?query='+term+'&queryIndex=suggestall&queryReturn=suggestall,idroot,auth,tag,type,raw,breaker,indicator&suggest=autoSubject&rows=20'
    #
    #     r = requests.get(url)
    #     res = json.loads(r.text)
    #     docs=res['response']['docs']
    #     # print(docs)
    #     for x in docs:
    #         suggest = x['suggestall'][0].lower()
    #         fastID = x['idroot']
    #
    #         score=fuzz.token_sort_ratio(term,suggest)
    #         print(score)
    #         writer.writerow({'filename': 'test', 'original_term': term, 'fast_term': suggest, 'fast_id': fastID, 'score':score})
                # print(fuzz.ratio(term,suggest))
