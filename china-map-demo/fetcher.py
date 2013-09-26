#!/usr/bin/env python
# -*- utf-8 -*-
#======================================================================

import os, re, json
import requests

#======================================================================

DIR_NAME      = os.path.dirname(__file__)
CITY_INFO_01  = os.path.join(DIR_NAME, 'city-info-01.txt')
FORMATTED     = os.path.join(DIR_NAME, 'city-info.json')
WEAHTER_QUERY = 'http://sou.qq.com/online/get_weather.php'
WEATHER_DB    = os.path.join(DIR_NAME, 'weather-db.json')

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

def get_city_list():
    with open(FORMATTED, 'r') as f:
        return json.loads(f.read())

def get_location_range(cl):
    max_latidude  = max([max([clause[1] for clause in cl[region]]) for region in cl.keys()])
    min_latitude  = min([min([clause[1] for clause in cl[region]]) for region in cl.keys()])
    max_longitude = max([max([clause[2] for clause in cl[region]]) for region in cl.keys()])
    min_longitude = min([min([clause[2] for clause in cl[region]]) for region in cl.keys()])
    return {'latidude' : (min_latitude , max_latidude),
            'longitude': (min_longitude, max_longitude)}

def get_weather(city_name):
    param = {'callback': 'Weather', 'city': city_name}
    resp = requests.get(WEAHTER_QUERY, params=param)
    match = re.search('^Weather\((?P<json>.*)\)\;$', resp.content.decode('utf-8'))
    data = json.loads(match.group('json'))
    return float(data['real']['temperature'])

def fetch_weather_list(cl):
    record = { 'success': {}, 'fail': [] }
    for region in cl.keys():
        for city in cl[region]:
            try:
                temp = get_weather(city[0])
                record['success'][city[0]]= temp
            except:
                record['fail'].append(city[0])
    with open(WEATHER_DB, 'w') as f:
        f.write(json.dumps(record))
    return record

#======================================================================

def main():
    cl = get_city_list()
    fetch_weather_list(cl)

#======================================================================

if __name__ == '__main__':
    main()
