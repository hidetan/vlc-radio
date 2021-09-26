#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# https://www.digitalradioplus.com.au/listen to m3u8
#

import os
import sys
import urllib3
from bs4 import BeautifulSoup

target_uri = 'https://www.digitalradioplus.com.au/listen'

outfile = os.getenv('dabp_au_playlist', '/tmp/dabp_au.m3u8')
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

f = open(os.path.join(outdir, 'digitalaudioplus_au.html'), 'w')
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

for li in soup.find_all("li", attrs = { "class": "stations-list-item" }):
    print("\n\n%s" % li, file = sys.stderr)
    station_name = li.find("h3", attrs = { "class": "station-name" }).get_text()
    station_summary = li.find("div", attrs = { "class": "station-summary" }).get_text()
    btn = li.find("button", attrs = { "class": "station-control js-station-control js-urlSelect" })
    if btn != None:
        stream_url = btn.get("data-stream-url")
    print("\t%s / %s\t%s" % (station_name, station_summary, stream_url), file = sys.stderr)
    if btn != None:
        f.write('#EXTINF:-1,%s / %s\n' % (station_name, station_summary))
        f.write('%s\n\n' % (stream_url))

f.close()

sys.exit(0)

