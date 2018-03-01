import csv
import sys
import requests
import json
from xml.etree import ElementTree as ET
# class SomeSillyAPI:
#     silly_example_data = [x for x in range(10000)]
#     hard_limit = 100
#
#     @classmethod
#     def gimme_data(cls, offset, limit=100):
#         if limit > cls.hard_limit:
#             limit = cls.hard_limit
#         return cls.silly_example_data[offset:offset+limit]

if __name__ == '__main__':
    # I want all the data, the API will only give me chunks

    # Start at the beginning
    offset = 0

    # Maybe I know the API limit - maybe I don't, I can set whatever I want
    limit = 100

    # Where I'm going to put it
    all_the_data = []

    # Lets get it

    # Loop over chunks
    while True:
        ecollections='https://api-eu.hosted.exlibrisgroup.com/almaws/v1/electronic/e-collections?view=full&expand=None&is_local=True&limit=100&offset='+str(offset)+'&apikey=xxxxx&format=json'
        # x=requests.get(ecollections)
        this_chunk = requests.get(ecollections)
        json_chunk = json.loads(this_chunk.text)

        # Did it return anything? If not the resource is exhausted, stop

        if len(json_chunk) == 0:
            break
        # # I asked for a lot - but the API has a limit, how much did I get?
        how_many_in_the_chunk = len(json_chunk)


        print(how_many_in_the_chunk)
        # # Now I want the ones after that
        offset = offset + how_many_in_the_chunk
        # # Add this chunk to our list of all of it
        all_the_data = all_the_data + json_chunk
#
print(all_the_data)
