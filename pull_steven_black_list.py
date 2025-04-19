#!/usr/bin/env python3

import http.client
import os
import util

source_domain = "raw.githubusercontent.com"
source_uri = "/StevenBlack/hosts/master/hosts"

def list_file() -> str:
    return util.reserve_cache_file('stevenBlack.list')

def cache():
    connection = http.client.HTTPSConnection(source_domain)
    connection.connect()
    connection.request("GET", source_uri, headers=util.get_headers())
    response = connection.getresponse()

    status = response.getcode()
    if status <= 200 and status < 300:
        with open(list_file(), 'w+') as output:
            started = False
            while line := response.readline():
                line = line.decode()
                line = line.strip()
                if len(line) == 0:
                    pass
                elif started and not line.startswith('#'):
                    split = line.split(' ', 1)
                    if(len(split) > 1):
                        domain = split[1]
                        output.write(domain + '\n')
                elif line.startswith('# Start StevenBlack'):
                    started = True

if __name__ == "__main__":
  cache()