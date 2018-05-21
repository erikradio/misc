import requests, json,csv,uuid,re
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
while True:
   
    gruyters_link = 'https://api-eu.hosted.exlibrisgroup.com/almaws/v1/electronic/e-collections/61172567390003843/e-services/62172567380003843/portfolios?limit=100&offset='+str(offset)+'&apikey=xxx&format=json'

    # print("GET {}".format(gruyters_link))
    this_chunk = requests.get(gruyters_link)
    # print(this_chunk.url)
    # this_chunk.raise_for_status()
    print("GET complete")
    print("Parsing as JSON")
    this_chunk_json = this_chunk.json()
    print("Parsed as JSON")
    # print(this_chunk_json)
#
    if this_chunk_json.get('portfolio') is None:
        raise RuntimeError("No records in the response!")
#
#     # Grab the total on the first run
    if total is None:
        total = this_chunk_json['total_record_count']
# #
#     # Count how many responses we got
    how_many_in_the_chunk = len(this_chunk_json['portfolio'])
    print(how_many_in_the_chunk)
#

#
#     # Gather the responses
    for record in this_chunk_json['portfolio']:
#
#
        if record['availability']['value'] == '10':
            portID = record['id']
            update_gruyter = 'https://api-eu.hosted.exlibrisgroup.com/almaws/v1/electronic/e-collections/61172567390003843/e-services/62172567380003843/portfolios/'+portID+'&apikey=xxx&format=json'

            # changeAvail=JsonPatch([{"op": "replace", "path":"/availability/value", "value":"11"}])
            # applyPatch=changeAvail.apply(record,in_place=True)
            # print(applyPatch)
            # print("Check to be sure this dict is fine")
            #
            # print("If this is the last thing printed serializing the patch to JSON causes the issue")
            # patchString=json.dumps(applyPatch)
            # updated_level=requests.put(update_gruyter, data=patchString)
            # print(updated_level.raise_for_status)
            #
            # print("Now we're interacting with the API, if this is the last thing printed then there is some connection problem")
            payload={'availability':{'value':'11','desc':'Available'}}
            updated_level=requests.put(update_gruyter, data=json.dumps(payload))
#
            print(updated_level.raise_for_status)
#             # print(updated_level.url)
#             # print("If this is the last thing printed then the API returned a bad response code")
#             # print(updated_level.text)
#             # response.raise_for_status()
#
#
#
#         all_the_data.append(record)
# #
#     # Increment our offset
    offset = offset + how_many_in_the_chunk
#
#     # End cases
    if how_many_in_the_chunk == 0 or len(all_the_data) == total:
        break
# dump_file = "test.json"
# with open(dump_file, 'w') as f:
#     json.dump(all_the_data, f)
# #
# #


# res = res.json()
# porto= res['portfolio']
# for x in porto:
#     print(x['availability']['value'])

    # print(x,y)
#     if x == 'id':
#         print(x)
# # get resource record
# record=requests.get(aspace_url+"/repositories/2/resources/2",headers=headers).json()

#get elements and values in record
# for key,value in record.items():
# 	if key=='level':
# 		#if the value is collection or something else
# 		if value=='collection':
# 			#change it to file
# 			test=JsonPatch([{"op": "replace", "path":"/level", "value":"file"}])
# 			applyPatch=test.apply(record,in_place=True)
# 		 	updated_level=requests.post(aspace_url+"/repositories/2/resources/2",headers=headers,data=json.dumps(applyPatch)).json()
