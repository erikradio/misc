import requests,sys,json,csv,uuid,re
from jsonpatch import JsonPatch
from re import match
from requests.auth import HTTPDigestAuth


solr_url = "http://localhost:8983/solr/masterfile/schema"
auth=()


# auth = requests.post(aspace_url+"users/"+auth[0]+"/login?password="+auth[1])
# auth.raise_for_status()
# auth_json=auth.json()
# session = auth_json["session"]
# headers = {"X-ArchivesSpace-Session":session}
# print(session)

# print(auth)

# print(headers)
with open(sys.argv[1],"rU") as csvFile:
    reader=csv.DictReader(csvFile)
    # print(reader.fieldnames)
    for x in reader.fieldnames:
        # print(x)
        new_fields = {"add-field":{"name":x,"type":"string","indexed":"true","stored":"true"}}
        # print(new_fields)
        field_post = requests.post(solr_url,data=json.dumps(new_fields)).json()
        print(field_post)
    # for row in reader[0]:
    #     print(row)

# new_fields = {"add-field":{"name":"marlowe","type":"string"}}

# field_post = requests.post(solr_url,data=json.dumps(new_fields)).json()
# print(field_post)

# getFields = requests.get(solr_url+'/fields')
# print(getFields.text)
