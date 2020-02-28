import json
import urllib.parse
from lxml import html as lx
import gzip
from io import BytesIO
import os
import logging
import csv
from time import time
import argparse
import sys
from pprint import pprint

file = sys.argv[1]

with gzip.open(file, 'rb') as html:
    body = html.read()

response = lx.fromstring(body)
print(len(body))
title = response.xpath('//meta[@property="og:title"]/@content')[0]
keywords = response.xpath('//meta[@property="og:video:tag"]/@content')
user_url = response.xpath('//span[@itemprop="author"]/link[@itemprop="url"]/@href')[0]
meta = response.xpath('//span[@class="video-time"]/span/text()')
print(len(meta))
meta = response.xpath('//h3[@class="yt-lockup-title "]/a/@title')

print(meta)
