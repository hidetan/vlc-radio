#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  radiko_playlist.py
#

import os
import sys
import urllib3
import xml.etree.ElementTree as ET

target_uri = 'https://radiko.jp/v3/station/region/full.xml'
outfile = os.getenv('radiko_playlist', '/tmp/radiko.m3u8')

outdir = os.path.dirname(outfile)

headers = {
    'User-Agent': os.getenv('http_user_agent',
                            'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0')
}

http = urllib3.PoolManager(4, headers = headers)
r = http.request('GET', target_uri)

print('r.status=', r.status)

if r.status != 200:
    sys.exit(1)

f = open(os.path.join(outdir, 'radiko_full.xml'), 'w')
f.write(r.data.decode('utf-8'))
f.close()

f = open(outfile, 'w');

f.write('#EXTM3U\n'
        '# -*- coding: utf-8 -*-\n'
        '\n'
        '#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----\n'
        '# %s\n'
        '#\n'
        '\n'
        % (target_uri))

ST = {}
root = ET.fromstring(r.data.decode('utf-8'))

for stations in root.iter('stations'):
    region_name = stations.attrib['region_name']

    for station in stations.iter('station'):
        station_id = station.find('id').text
        station_name = station.find('name').text
        area_id = station.find('area_id').text
        ST[station_id] = { 'name': station_name, 'id': area_id }

        title = '#EXTINF:-1,%s / %s %s %s\n' % (region_name, station_name, station_id, area_id)
        uri = 'https://radiko.jp/v2/api/ts/playlist.m3u8?station_id=%s&l=15\n\n' % (station_id)

        print(title, end = '')
        f.write(title)

        print(uri, end = '')
        f.write(uri)

f.close()

sys.exit(0)

