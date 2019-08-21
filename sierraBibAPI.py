import requests, json, csv, sys


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



def get_count(s, bibLevel):

    jsonQuery = {
      "target": {
        "record": {
          "type": "bib"
        },
        "id": 30
      },
      "expr": {
        "op": "equals",
        "operands": [
          bibLevel,
          ""
        ]
      }
    }


    offset = 0
    url = 'https://libraries.colorado.edu:443/iii/sierra-api/v5/bibs/query?offset='+str(offset)+'&limit=1000'
    while True:
        r = s.post(url, json=jsonQuery)
        r.raise_for_status()
        rjson = r.json()
        currentCount = rjson['total']

        offset = offset +currentCount
        url = 'https://libraries.colorado.edu:443/iii/sierra-api/v5/bibs/query?offset='+str(offset)+'&limit=1000'
        # print(url)

        # print(currentCount)
        if currentCount < 1000:
            break
        # if peak(s, url) is False:
        #     print(rjson)
        #     break
    return offset


def peak(s, url):
    r = s.head(url)
    try:
        r.raise_for_status()  # Not a 404 - the next page exists
        return True
    except:
        return False


def main():
    bibLevels = ["a","o","t"]
    session = get_session()
    for x in bibLevels:
        count = get_count(session, x)
        print(x + ": " + str(count))




if __name__ == '__main__':
    main()
