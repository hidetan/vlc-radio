#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# listenradio_playlist.py
#

import os
import re
import sys
import urllib3
from bs4 import BeautifulSoup

target_uri = 'https://listenradio.jp/Home/Channel'

outfile = os.getenv('listenradio_playlist', '/tmp/listenradio.m3u8')
outdir = os.path.dirname(outfile)

headers = {
    'User-Agent': os.getenv('http_user_agent',
                            'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'),
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://listenradio.jp',
    'Referer': 'https://listenradio.jp/',
}

http = urllib3.PoolManager(4, headers = headers)
r = http.request('POST',
                 target_uri,
                 fields = { 'categoryId': '10005', 'areaId': '' })

print('r.status=', r.status)

if r.status != 200:
    sys.exit(1)

f = open(os.path.join(outdir, 'listenradio.html'), 'w')
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

for cl_li in soup.find_all('li', attrs = { 'class': re.compile('showChannelList*') }):
#    print(cl_li)
    cl_id = cl_li.get('id')
    cl_label = cl_li.select_one('span', attrs = { 'class': 'arrow' }).get_text()
    print('[%s]: %s' % (cl_id, cl_label), file = sys.stderr)

    for li in soup.find_all('li', attrs = { 'class': 'channelList' + cl_id }):
#        print(li.get('class')[0])
        station_label = li.select_one('div', attrs = { 'class:' 'wrap' }).get_text().replace('\n', '').replace('\r', '')
        station_url = li.get('url')
        station_url = station_url.replace('manifest.f4m', 'playlist.m3u8')
        print('\t%s\t%s' % (station_label, station_url), file = sys.stderr)
        title = '#EXTINF:-1,%s / %s\n' % (station_label, cl_label)
        uri = '%s\n\n' % (station_url)

        print(title, end = '')
        f.write(title)
        print(uri, end = '')
        f.write(uri)

f.close()

sys.exit(0)

