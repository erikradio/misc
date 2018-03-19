import requests, sys
import json

# Define the Alma URL to be called - in this case the acq API
url = 'https://api-na.hosted.exlibrisgroup.com/almaws/v1/acq/vendors'

# Specify query paramaters to the URL (json output and the APIKEY for the configuration API)


params = {'content-type':'application/json', apikey':'xxxx'}

# get the JSON data
with open(sys.argv[1]) as f:
    # print(f.read()[0])
    values = json.load(f)
    # print(values)
for vendor in values['vendors']:
    print(vendor)
    # print(vendor)

# Make the post
    # r = requests.post(url, data=vendor, params=params)
    # print(r.json())


# If the next line raises an error our request returned an error code
# if the line after raises an error it didn't return JSON, but did
# come back with a 200 status
    # r.raise_for_status()
# The following line is for debugging
#print(postrequest.text)
    # json_response = r.json()
    # print(json_response)
