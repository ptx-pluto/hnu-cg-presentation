#!/usr/bin/env python
# -*- utf-8 -*-
#=====================================================================================================

import os, re, json
import requests
from os.path import join, dirname, abspath

#=====================================================================================================

DATA_ROOT     = join(dirname(dirname(abspath(__file__))), 'data')
CITY_INFO_01  = join(DATA_ROOT, 'city-info-01.txt')
FORMATTED     = join(DATA_ROOT, 'city-info.json')
WEATHER_DB    = join(DATA_ROOT, 'weather-db.json')

WEAHTER_QUERY = 'http://sou.qq.com/online/get_weather.php'

#=====================================================================================================
# Construct city list
#=====================================================================================================

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

def get_city_list():
    with open(FORMATTED, 'r') as f:
        return json.loads(f.read())

#=====================================================================================================
# Construct weather list
#=====================================================================================================

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

#=====================================================================================================
# Complete the list containing all information needed for plotting
#=====================================================================================================

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

#=====================================================================================================
# Analyze metadata
#=====================================================================================================

def get_range(al):
    max_lati = max([record['latitude'] for record in al])
    min_lati = min([record['latitude'] for record in al])
    max_long = max([record['longitude'] for record in al])
    min_long = min([record['longitude'] for record in al])
    max_temp = max([record['temp'] for record in al])
    min_temp = min([record['temp'] for record in al])
    return {'latidude' : (min_lati, max_lati),
            'longitude': (min_long, max_long),
            'temp'     : (min_temp, max_temp)}

#=====================================================================================================

def test():
    al = get_all()
    r = get_range(al)

#=====================================================================================================

if __name__ == '__main__':
    pass
