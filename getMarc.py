import requests, json, csv, sys


key = ''
secret = ''
tags =['110','111','245','130','240','247','780','781','785','260','264','255','257','650','651','652','653','690','691',
'310','315','321','336','338','337','338','342','343','306','344','346','347','350','352','362','380','381','382','383','384','655','440','490',
'800','810','811','830','502','504','505','506','508','511','520','521','522','525','533','538','539','541','546','550','555','561','583','586',
'588','765','767','770','772','773','775','776','777','787','700','710','711','210','246','730','740','793','510','020','022','028','072','536',
'910','001','019','086','050','856','857','859']

newTags = []
def add_to_data_dict(d, key, value):
    if key not in d:
        d[key] = []
    if value not in d[key]:
        d[key].append(value)


# Containing data structure
bibDatas = []

# Establish HTTP the session
s = requests.Session()
resp = s.post('https://libraries.colorado.edu:443/iii/sierra-api/v5/token', auth=(key, secret))
resp.raise_for_status()
bearer_token = resp.json()['access_token']
# Set auth token for future requests.
s.headers["Authorization"] = "Bearer {}".format(bearer_token)

with open(sys.argv[1],'r') as csvFile:
    for row in csv.DictReader(csvFile):
        bibData = {}
        # Compute the URL
        bib = row['bib'].replace('b','')
        # bib = row['PermaLink'].replace('http://libraries.colorado.edu/record=b','')
        # bib = bib[:-3]
        url = 'https://libraries.colorado.edu:443/iii/sierra-api/v5/bibs/'+bib+'/marc'
        # Get the result
        r = s.get(url, headers={'Accept':'application/marc-in-json'})

        # Ignore dead links
        if r.status_code == 404:
            pass

        # Get JSON data from the request
        json_data = json.loads(r.text)  # TODO: Check if this can be r.json()
        bibData['eventAction'] = row['Event Action']
        bibData['bibID'] = row['bib']
        bibData['url'] = row['bibURL']
        bibData['EventLabel'] = row['Event Label']
        bibData['clicks'] = row['clicks']
        bibData['views'] = row['views']
        if 'fields' in json_data:
            # print(json_data)
            for datafield in json_data['fields']:
                for marcTag in datafield:
                    if 'subfields' in datafield[marcTag] and marcTag in tags:
                        for code_dict in datafield[marcTag]['subfields']:
                            for code_key in code_dict:
                                key = marcTag + code_key
                                value = code_dict[code_key]
                                newTags.append(key)
                                print(key,value)
                                add_to_data_dict(bibData, key, str(value))
        bibDatas.append(bibData)
        # print(bibDatas)

    # print(newTags)
master_dict = {}
for d in bibDatas:
    # print(d)
    for k in d:
        # print(k)
        if k not in master_dict:
            master_dict[k] = []
        for value in d[k]:
            if value not in master_dict[k]:
                # master_dict[k].append(value)
                master_dict[k] = value
                # print(d[k])
# print(master_dict)
newTags = list(set(newTags))
with open('bibs.csv','w') as outfile:

    fieldnames = ['eventAction', 'bibID', 'url', 'eventLabel', 'clicks', 'views'] + newTags
    writer = csv.DictWriter(outfile, fieldnames=fieldnames, restval='', extrasaction='ignore')
    writer.writeheader()
    for row in bibDatas:
        # print(row)
        row = {x: "|".join(row[x]) for x in row}
        # print(row)
        writer.writerow(row)
# with open('bibs.csv','w') as outfile:
#
#     rows = []
#     headers = list(master_dict.keys())
#     rows.append(headers)
#     writer = csv.DictWriter(outfile, fieldnames=headers)
#     for row in master_dict:
#         print(row)
#         writer.writerow(row)

# def write_list_of_dicts_to_file(outfile_path, out_rows, field_names):
#     """
#     __Args__
#     1. outfile_path (str): The path to the output file
#     2. out_rows (list): A list of dictionaries containing data
#     3. field_names (list): A list of strings containing field names
#         which are present in EVERY dictionary in the out_rows array
#     """
#     with open(outfile_path, 'w') as resultsFile:
#         writer = csv.DictWriter(resultsFile, field_names)
#         writer.writeheader()
#         for out_row in out_rows:
#             writer.writerow(out_row)
