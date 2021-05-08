#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# radiko_playlist.py
#

import os
import sys
import urllib3
import xml.etree.ElementTree as ET

target_uri = 'https://www.nhk.or.jp/radio/config/config_web.xml'
outfile = os.getenv('nhk_playlist', '/tmp/nhk.m3u8')

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

f = open(os.path.join(outdir, 'nhk_config_web.xml'), 'w')
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

for data in root.iter('data'):
    area_name = data.find('areajp').text

    for channel in [ { 'name': 'NHK 第一', 'tag': 'r1hls' },
                     { 'name': 'NHK 第二', 'tag': 'r2hls' },
                     { 'name': 'NHK FM'  , 'tag': 'fmhls' }, ]:

        title = '#EXTINF:-1,%s / %s\n' % (area_name, channel['name'])
        uri = '%s\n\n' % data.find(channel['tag']).text

        print(title, end = '')
        f.write(title)

        print(uri, end = '')
        f.write(uri)

f.close()

sys.exit(0)

