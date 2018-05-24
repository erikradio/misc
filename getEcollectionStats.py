import requests, json, csv,uuid,re
from jsonpatch import JsonPatch
from re import match

# Start at the beginning
offset = 0

# Maybe I know the API limit - maybe I don't, I can set whatever I want
limit = 100

# Where I'm going to put it
all_the_data = []

# get all resource ids
total = None
# while True:
#     # headers = {'apikey':'l7xx70b8ebb20fe94d4aa6fe7e5d540733d1'}
#     ecollections='https://api-na.hosted.exlibrisgroup.com/almaws/v1/electronic/e-collections?view=full&expand=None&is_local=True&limit=100&offset='+str(offset)+'&apikey=xxx&format=json'
#
#     # print("GET {}".format(gruyters_link))
#     this_chunk = requests.get(ecollections)
#     # print(this_chunk.url)
#     # this_chunk.raise_for_status()
#     # print("GET complete")
#     # print("Parsing as JSON")
#     this_chunk_json = this_chunk.json()
#     # print("Parsed as JSON")
#     # print(this_chunk_json)
# #
#     if this_chunk_json.get('electronic_collection') is None:
#         raise RuntimeError("No records in the response!")
# #
# #     # Grab the total on the first run
#     if total is None:
#         total = this_chunk_json['total_record_count']
# # #
# #     # Count how many responses we got
#     how_many_in_the_chunk = len(this_chunk_json['electronic_collection'])
#     # print(how_many_in_the_chunk)
#     print(this_chunk_json)

with open('almaCollections.json','r') as jsonfile:
    data = json.load(jsonfile)
    for record in data:
        id = record['id']
        publicName = record['public_name']
        portfolioCount = record['portfolios']['value']
        services = 'https://api-eu.hosted.exlibrisgroup.com/almaws/v1/electronic/e-collections/'+id+'/e-services?apikey=xxx&format=json'
        getService = requests.get(services)
        service_json=getService.json()
        for x in service_json['electronic_service']:
            if x['type']['value'] == 'getFullTxt':
                eserviceID=x['id']

            portURL = 'https://api-eu.hosted.exlibrisgroup.com/almaws/v1/electronic/e-collections/'+id+'/e-services/'+eserviceID+'/portfolios?limit=100&offset='+str(offset)+'&apikey=xxx&format=json'
            getPort = requests.get(portURL)
            portList = getPort.json()
            activeCount = []
            for record in portList['portfolio']:

                if record['availability']['value'] == '11':
                    print(record['availability']['value'])

        # print(getService.text)
#
#     # Gather the responses
    # for record in this_chunk_json:
    #     print(record)
#
#
#         if record['availability']['value'] == '10':
#
#             portID = record['id']
#             print(portID)
#             update_gruyter = 'https://api-eu.hosted.exlibrisgroup.com/almaws/v1/electronic/e-collections/61172567390003843/e-services/62172567380003843/portfolios/'+portID+'?&apikey=xxx'
#             #METHOD1
#             # changeAvail=JsonPatch([{"op": "replace", "path":"/availability/value", "value":"11"}])
#             # applyPatch=changeAvail.apply(record,in_place=True)
#             # print(applyPatch)
#             # print("Check to be sure this dict is fine")
#             #
#             # print("If this is the last thing printed serializing the patch to JSON causes the issue")
#             # patchString=json.dumps(applyPatch)
#             # updated_level=requests.put(update_gruyter, data=patchString)
#             # print(updated_level.raise_for_status)
#             #
#             #METHOD2
#             # print("Now we're interacting with the API, if this is the last thing printed then there is some connection problem")
#             headers = {"content-type": "application/json"}
#             payload={'availability':{'value':'11','desc':'Available'}}
#             updated_level=requests.put(update_gruyter, json=payload, headers=headers)
#             print(updated_level.url)
#             print(updated_level.status_code)
#             print(updated_level.reason)
#             print(updated_level.text)
#
# #
#             # print(updated_level.raise_for_status)
# #             # print(updated_level.url)
# #             # print("If this is the last thing printed then the API returned a bad response code")
# #             # print(updated_level.text)
# #             # response.raise_for_status()
# #
# #
# #
#         all_the_data.append(record)
# # #
# #     # Increment our offset
#     offset = offset + how_many_in_the_chunk
# #
# #     # End cases
#     if how_many_in_the_chunk == 0 or len(all_the_data) == total:
#         break
#
# dump_file = "ecollectionStats.csv"
# with open(dump_file, 'w') as f:
#     json.dump(all_the_data, f)
