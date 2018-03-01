# -*- coding: utf-8 -*-
import json
from urllib.parse import quote

import requests


traversed_ids = []

# THIS WILL LOAD EVERY RECORD INTO RAM AT ONCE /disclaimer


def debug_request_error(resp):
    debug_dict = {}
    debug_dict['status_code'] = resp.status_code
    try:
        debug_dict['response'] = resp.json()
    except:
        try:
            debug_dict['response'] = str(resp.data())
        except:
            debug_dict['response'] = None
    raise RuntimeError(
        "An error has occured, report follows:\n{}".format(
            json.dumps(debug_dict, indent=4)
        )
    )


def response_200_json(resp):
    if resp.status_code != 200:
        debug_request_error(resp)
    try:
        rj = resp.json()
    except:
        raise RuntimeError(
            "Response was not JSON!"
        )
    return rj


def get_it_all(api_endpoint):
    results = []
    try:
        api_resp = requests.get(api_endpoint)
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "The GET request failed, the webserver is down or " +
            "closed the connection on us."
        )
    r = response_200_json(api_resp)
    if r['status'] != "ok":
        debug_request_error(api_resp)
    # Records that don't have a next cursor don't have the field
    # at all, so use a call to .get with None as the default
    # in order to avoid KeyErrors being raised
    next_cursor = False
    next_cursor = r.get('message', {}).get('next-cursor', False)
    if next_cursor:
        # Prevent circular paths
        global traversed_ids
        if next_cursor not in traversed_ids:
            traversed_ids.append(next_cursor)
            print(next_cursor)
            # Recursion case
            # Gather up anything from the next records
            results = results + get_it_all(
                construct_url_from_next_cursor(next_cursor)
            )
    # Gather up everything from this record
    # We have to be sure this field exists first though
    # This is a really big hack with nested gets
    # Probably don't actually ever do this
    if r.get('message', {}).get('items', False):
        for x in r['message']['items']:
            results.append(x)
    print(len(results))
    return results


def construct_url_from_next_cursor(next_cursor):
    # do stuff here
    # return a valid url as a string
    api_endpoint = \
        'http://api.crossref.org/prefixes/10.2458/works?rows=1000&cursor=*'
    return api_endpoint[0:-1] + quote(next_cursor)


def main():
    api_endpoint = \
        'http://api.crossref.org/prefixes/10.2458/works?rows=1000&cursor=*'
    with open('results.json', 'w') as f:
        json.dump(get_it_all(api_endpoint), f)


if __name__ == "__main__":
    main()
