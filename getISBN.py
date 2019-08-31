import requests, json, csv, sys
from datetime import datetime
import copy, time, datetime


def get_session():
    key = ''
    secret = ''
    headers={"Content-Type":  "application/json"}

    s = requests.Session()
    resp = s.post( 'https://libraries.colorado.edu:443/iii/sierra-api/v5/token', auth=(key, secret))
    resp.raise_for_status()
    bearer_token = resp.json()['access_token']
    # print(bearer_token)
    # get auth token out of the response
    s.headers["Authorization"] = "Bearer {}".format(bearer_token)
    return s



def get_isbn(s, isbn):
    url = 'https://libraries.colorado.edu:443/iii/sierra-api/v5/bibs/search?fields=id,title,author,materialType,locations&index=isbn&text='+isbn
    # print(url)
    # url = 'https://libraries.colorado.edu:443/iii/sierra-api/v5/bibs/search?fields=title,author,publishYear&index=isbn&text='+isbn
    bibData={}
    r = s.get(url)
    r.raise_for_status()
    rjson = r.json()
    if rjson['count'] == 0:
        bibData['bibID'] = 'Not Available'
        bibData['isbn'] = isbn

    if rjson['count'] == 1:
        bibData['bibID'] = rjson['entries'][0]['bib']['id']
        bibData['isbn'] = isbn
        bibData['title'] = rjson['entries'][0]['bib']['title']
        bibData['author'] = rjson['entries'][0]['bib']['author']
        bibData['format'] = rjson['entries'][0]['bib']['materialType']['value']
        bibData['locations'] = rjson['entries'][0]['bib']['locations'][0]['name']
        # print(rjson['entries'][0]['bib']['materialType']['value'])
        if rjson['entries'][0]['bib']['materialType']['value'] != 'eBooks' :
            itemURL = 'https://libraries.colorado.edu:443/iii/sierra-api/v5/items/?bibIds='+bibData['bibID']
            # itemURL = 'https://libraries.colorado.edu:443/iii/sierra-api/v5/items/'+bibData['bibID']+'?fields=status,callNumber'
            r2 = s.get(itemURL)
            rjson2 = r2.json()
            # print(rjson2)
            if 'entries' in rjson2:
                for entry in rjson2['entries']:
                    if 'location' in entry:
                        bibData['availability'] = entry['location']['name']+'-'+entry['status']['display']+'|'
                    if 'callNumber' in entry:
                        bibData['callNumber'] = entry['callNumber']
                    print(bibData['availability'])
        # print(rjson2)

    return(bibData)

def main():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    with open(sys.argv[1],'r') as courseList, open('bibData_'+str(st)+'.csv','w') as outfile:
        session = get_session()
        reader = csv.DictReader(courseList)
        fieldnames = ['bibID','isbn','title','author','format','locations','availability','callNumber']
        w = csv.DictWriter(outfile, fieldnames)
        w.writeheader()
        for row in reader:
            isbn = row['ISBN']

            bib = get_isbn(session, isbn)

            #
            w.writerow(bib)
            # print(bib)
            # print(x + ": " + str(count))




if __name__ == '__main__':
    main()
