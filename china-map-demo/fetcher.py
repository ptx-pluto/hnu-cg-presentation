#!/usr/bin/env python
# -*- utf-8 -*-
#======================================================================

import os, re, json
import requests
from os.path import join, dirname

#======================================================================

DATA_ROOT     = join(dirname(dirname(__file__)), 'data')
CITY_INFO_01  = join(DATA_ROOT, 'city-info-01.txt')
FORMATTED     = join(DATA_ROOT, 'city-info.json')
WEATHER_DB    = join(DATA_ROOT, 'weather-db.json')

WEAHTER_QUERY = 'http://sou.qq.com/online/get_weather.php'

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

def fetch_weather_list(cl, db=True):
    if db:
        try:
            with open(WEATHER_DB, 'r') as f:
                return json.loads(f.read())
        except:
            pass
    record = { 'success': {}, 'fail': [] }
    for region in cl.keys():
        for city in cl[region]:
            try:
                temp = get_weather(city[0])
                record['success'][city[0]] = temp
            except:
                record['fail'].append(city[0])
    with open(WEATHER_DB, 'w') as f:
        f.write(json.dumps(record))
    return record

#======================================================================

def get_all():
    cl = get_city_list()
    wl = fetch_weather_list(cl)
    al = []
    for region in cl:
        for city, latitude, longitude in cl[region]:
            if city in wl['success']:
                al.append(dict(city=city, 
                               temp=wl['success'][city], 
                               latitude=latitude, 
                               longitude=longitude))
    return al

#======================================================================

if __name__ == '__main__':
    pass
