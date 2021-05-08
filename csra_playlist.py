#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# csra_playlist.py
#

import os
import sys
import urllib3
from bs4 import BeautifulSoup

target_uri = 'http://csra.fm/stationlist/'

outfile = os.getenv('csra_playlist', '/tmp/csra.m3u8')
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

f = open(os.path.join(outdir, 'csra.html'), 'w')
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

for s in soup.find_all("section"):
    print("-----", file = sys.stderr)
#    print(s, file = sys.stderr)

    label = s.find("h1")
    location = s.find("p")
    a = s.find('a', attrs = { 'class': 'stm' })

    if label != None:
        print("LABEL: %s" % label.get_text(), file = sys.stderr)
    if location != None:
        print("LOCATION: %s" % location.get_text(), file = sys.stderr)

    uri = None
    if a != None:
        print("A: %s" % a, file = sys.stderr)
        if not 'listenradio.jp' in a['href']:
            uri = a['href']

    if label != None and location != None and uri != None:
        title = '#EXTINF:-1,%s / %s\n' % (label.get_text(), location.get_text())
        uri = '%s\n\n' % uri

        print(title, end = '')
        f.write(title)
        print(uri, end = '')
        f.write(uri)

f.close()

sys.exit(0)

