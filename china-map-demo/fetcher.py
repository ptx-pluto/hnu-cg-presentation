#!/usr/bin/env python
# -*- utf-8 -*-
#======================================================================

import os, re, json

#======================================================================

DIR_NAME     = os.path.dirname(__file__)
CITY_INFO_01 = os.path.join(DIR_NAME, 'city-info-01.txt')
FORMATTED = os.path.join(DIR_NAME, 'city-info.json')

#======================================================================

def format_city_info():
    record = {}
    with open(CITY_INFO_01, 'r') as f:
        for line in f.readlines():
            region, city, latitude, longitude = line.split()
            latitude  = float((re.search('^北纬(?P<latitude>.*)$' , latitude )).group('latitude'))
            longitude = float((re.search('^东经(?P<longitude>.*)$', longitude)).group('longitude'))
            if region not in record:
                record[region] = []
            record[region].append((city, latitude, longitude))
    with open(FORMATTED, 'w') as f:
        f.write(json.dumps(record))

#======================================================================

if __name__ == '__main__':
    format_city_info()
