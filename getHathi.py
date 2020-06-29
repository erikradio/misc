import requests, json, csv, sys
from fuzzywuzzy import fuzz, process
from xml.etree.ElementTree import Element, SubElement, Comment, tostring

def getHT(oclc):
    # with open(sys.argv[1],'r') as incsv:
        # reader = csv.DictReader(incsv)
        # for row in reader:


        url = 'http://catalog.hathitrust.org/api/volumes/brief/oclc/' + oclc + '.json'
        # print(url)


        htDict = {}


        r = requests.get(url)
        r.raise_for_status()
        docs=r.json()
        if docs['records']:

            for record in docs['records']:

                recordURL = docs['records'][record]['recordURL']
                title = docs['records'][record]['titles'][0]
                isbns = docs['records'][record]['isbns']
                isbn = ''
                if len(isbns) > 0:
                    htDict['isbn'] = isbns[0]
                else:
                    htDict['isbn'] = ''
            htDict['recordURL'] = recordURL
            htDict['title'] = title
            # htDict['isbn'] = isbn
            htDict['oclc'] = oclc

        else:

            htDict['oclc'] = oclc



        # print(htDict)
        return htDict

def main():
    with open(sys.argv[2],'w') as outcsv, open(sys.argv[1],'r') as incsv:

        writer = csv.DictWriter(outcsv, fieldnames = ["title", "oclc", "isbn", "recordURL"])
        writer.writeheader()
        reader = csv.DictReader(incsv)
        for row in reader:
            oclc = row['oclc']



            thing=getHT(oclc)
            print(thing)
            writer.writerow(thing)
            # for x in thing:
            #     print(x)
            # print(thing)

if __name__ == '__main__':

    main()
