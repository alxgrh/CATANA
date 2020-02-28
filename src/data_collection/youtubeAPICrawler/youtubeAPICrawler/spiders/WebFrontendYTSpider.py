import scrapy
from scrapy import signals
import logging
import urllib
import json
import time
import shlex
import itertools
import random
import os
import gzip
from lxml.html.clean import clean_html
from lxml import html as lx

from youtubeAPICrawler.items import *

from catana import settings # YOUTUBE_API_KEY, YOUTUBE_CHANNEL_LIST


class PopulateYTSpider(scrapy.Spider):
    
    name = "webspider"
    # use these settings per spider, so different spider different pipelines
    custom_settings = {
        'ITEM_PIPELINES': {
            'youtubeAPICrawler.pipelines.PopulateDatabasePipeline': 900,
        }
    }
    #'youtubeAPICrawler.pipelines.ChannelItemPipeline': 300,
    #'youtubeAPICrawler.pipelines.VideoListItemPipeline': 300,

    allowed_domains = ["www.youtube.com"]

    MAX_SEARCH_DEPTH = 0 # Crawl the related channel of our provided channel

    YOUTUBE_CHANNEL_LIST = settings.YOUTUBE_CHANNEL_LIST

    DATA_DIR = settings.DATA_STORAGE_PATH
    
    def start_requests(self):
        
        with open(self.YOUTUBE_CHANNEL_LIST, 'r') as f:
            channels = json.load(f)
        
        urls = [ f'https://www.youtube.com/channel/{channel_id.strip()}' for channel_id in channels ]
        
        for url in urls:
            request = scrapy.Request(url=url, callback=self.parse_channel)
            yield request
    
    def parse_channel(self,response):
        channel_id = response.url.split('/')[-1]
        name = f"{os.path.join(self.DATA_DIR,channel_id)}.html.gz"
        with gzip.open(name, 'wb') as f:
            f.write(response.body)
        
        response = lx.fromstring(response.body)
        user_url = response.xpath('//span[@itemprop="author"]/link[@itemprop="url"]/@href')[0]
        title = response.xpath('//meta[@property="og:title"]/@content')[0]
        keywords = response.xpath('//meta[@property="og:video:tag"]/@content')
        description = response.xpath('//meta[@property="og:description"]/@content')[0]
        
        yield ChannelItem(
                id = channel_id,
                title = title,
                keywords = keywords,
                description = description,
                dateAdded = time.strftime('%Y-%m-%d %H:%M:%S') ,
                featuredChannelsIDs = [],
                uploadsPlaylistID = '',
                unsubscribedTrailer = '',
                topicIds = [],
                crawlTimestamp = time.strftime('%Y-%m-%d %H:%M:%S') 
            )
        request = scrapy.Request(user_url.replace('http:','https:')+'/videos?disable_polymer=1', callback=self.parse_videos_list, meta={'channel_id':channel_id})
        yield request

    def parse_videos_list(self,response):
        name = f"{os.path.join(self.DATA_DIR,response.url.split('/')[-2])}.videos.html.gz"
        with gzip.open(name, 'wb') as f:
            f.write(response.body)
        
        channel_id = response.meta['channel_id']
        response = lx.fromstring(response.body)
        videos = response.xpath('//h3[@class="yt-lockup-title "]/a/@href')
        titles = response.xpath('//h3[@class="yt-lockup-title "]/a/@title')
        for i,video in enumerate(videos):
            yield  VideoItem(
                id = video.split('=')[-1],
                channelID = channel_id,
                title = titles[i],
                description = '',
                category = 26,
                duration = '',
                dateAdded = '',
                tags = [],
                topicIds = [],
                crawlTimestamp = time.strftime('%Y-%m-%d %H:%M:%S') 
            )
            
    
        