#!/usr/bin/env python3

import http.client
import util
import json

source_domain = "staticcdn.duckduckgo.com"
source_uri = "/trackerblocking/v2.1/tds.json"
block_all = True

def json_file() -> str:
    return util.reserve_cache_file('duckDuckGo.json')

def list_file() -> str:
    return util.reserve_cache_file('duckDuckGo.list')

def cache_json():
    connection = http.client.HTTPSConnection(source_domain)
    connection.connect()
    connection.request("GET", source_uri, headers=util.get_headers())
    response = connection.getresponse()

    status = response.getcode()
    if status <= 200 and status < 300:
        with open(json_file(), 'w+') as output:
            while line := response.readline():
                output.write(line.decode())
    else:
        print('Error, got status ' + str(status))

def parse():
    with open(json_file(), 'r') as input:
        data = json.loads(input.read())
        trackers = data['trackers']
        with open(list_file(), 'w+') as output:
            for values in trackers.values():
                if block_all or values['default'] == 'block':
                    output.write(values['domain'] + '\n')

if __name__ == "__main__":
    cache_json()
    parse()
