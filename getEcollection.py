import requests
import json

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
    total = None
    while True:
        ecollections='https://api-na.hosted.exlibrisgroup.com/almaws/v1/electronic/e-collections?view=full&expand=None&is_local=True&limit=100&offset='+str(offset)+'&apikey=l7xx70b8ebb20fe94d4aa6fe7e5d540733d1&format=json'
        print("GET {}".format(ecollections))
        this_chunk = requests.get(ecollections)
        this_chunk.raise_for_status()
        print("GET complete")
        print("Parsing as JSON")
        this_chunk_json = this_chunk.json()
        print("Parsed as JSON")

        # Validate our response has records in it, otherwise throw
        # an exception
        if this_chunk_json.get('electronic_collection') is None:
            raise RuntimeError("No records in the response!")

        # Grab the total on the first run
        if total is None:
            total = this_chunk_json['total_record_count']

        # Count how many responses we got
        how_many_in_the_chunk = len(this_chunk_json['electronic_collection'])

        # Gather the responses
        for record in this_chunk_json['electronic_collection']:
            all_the_data.append(record)

        # Increment our offset
        offset = offset + how_many_in_the_chunk

        # End cases
        if how_many_in_the_chunk == 0 or len(all_the_data) == total:
            break

    dump_file = "test.json"
    with open(dump_file, 'w') as f:
        json.dump(all_the_data, f)
