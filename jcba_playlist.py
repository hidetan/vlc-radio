#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# jcba_playlist.py
#

import os
import sys
import urllib3
from bs4 import BeautifulSoup

target_uri = 'https://www.jcbasimul.com'

outfile = os.getenv('jcba_playlist', '/tmp/jcba.m3u8')
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

f = open(os.path.join(outdir, 'jcbasimul.html'), 'w')
html_data = r.data.decode('utf-8')
f.write(html_data)
f.close()

soup = BeautifulSoup(html_data, 'lxml')

f = open(outfile, 'w');

f.write('#EXTM3U\n'
        '# -*- coding: utf-8 -*-\n'
        '\n'
        '#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----\n'
        '# %s\n'
        '#\n'
        '\n'
        % (target_uri))

no = 0

for al in soup.find_all('div', attrs = { 'class': 'areaList' }):
    print('-----', file = sys.stderr)
    print(al, file = sys.stderr)
    for li in al.select('li'):
#        print(li)
        station_label = li.get('value').replace('&', '&amp;')
        station_id = li.find('div', attrs = { 'class': 'rplayer' }).get('id')
        print('%s : %s' % (station_label, station_id), file = sys.stderr)

        title = '#EXTINF:-1,%s\n' % (station_label)
        uri = 'https://musicbird-hls.leanstream.co/musicbird/%s.stream/playlist.m3u8\n\n' % (station_id)

        print(title, end = '')
        f.write(title)

        print(uri, end = '')
        f.write(uri)

f.close()

sys.exit(0)

