# -*- coding: utf-8 -*-

# MIT License
# 
# Copyright (c) 2017 Moritz Lode
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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

def quoteSplit(value):
    lex = shlex.shlex(value)
    lex.quotes = '"'
    lex.whitespace_split = True
    lex.commenters = ''
    return list(lex)

from youtubeAPICrawler.items import *

from catana import settings # YOUTUBE_API_KEY, YOUTUBE_CHANNEL_LIST

class PopulateYTSpider(scrapy.Spider):
    '''
    Populates the Database with Youtube meta data of the provided channels from channelIDs.txt
    and their related channels see MAX_SEARCH_DEPTH

    API Unit costs: 12 Points per Channel
    '''
    
    name = "populate"
    # use these settings per spider, so different spider different pipelines
    custom_settings = {
        'ITEM_PIPELINES': {
            'youtubeAPICrawler.pipelines.PopulateDatabasePipeline': 900,
        }
    }
    #'youtubeAPICrawler.pipelines.ChannelItemPipeline': 300,
    #'youtubeAPICrawler.pipelines.VideoListItemPipeline': 300,

    allowed_domains = ["www.googleapis.com"]

    MAX_SEARCH_DEPTH = 0 # Crawl the related channel of our provided channel

    YOUTUBE_API_KEY = settings.YOUTUBE_API_KEY
    YOUTUBE_API_KEYS = []
    YOUTUBE_API_KEY_LIST = settings.YOUTUBE_API_KEY_LIST

    YOUTUBE_CHANNEL_LIST = settings.YOUTUBE_CHANNEL_LIST

    YOUTUBE_API_CHANNEL_URL = 'https://www.googleapis.com/youtube/v3/channels'
    YOUTUBE_API_SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'
    YOUTUBE_API_PLAYLISTITEMS_URL = 'https://www.googleapis.com/youtube/v3/playlistItems'  
    YOUTUBE_API_VIDEO_URL = 'https://www.googleapis.com/youtube/v3/videos'


    def get_api_key(self):
        return random.choice(self.YOUTUBE_API_KEYS)
    '''
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(PopulateYTSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider


    def spider_closed(self, spider):
        spider.logger.info('Spider closed yoooo: %s', spider.name)
    '''

    def start_requests(self):
        '''
        returns iterable of Requests, either list or generator, which will be begin to crawled
        '''
        urls = []

        # Generate API keys list
        if os.path.isfile(self.YOUTUBE_API_KEY_LIST):
            with open(self.YOUTUBE_API_KEY_LIST) as api_keys:
                for key in json.load(api_keys):
                    self.YOUTUBE_API_KEYS.append(key)
        else:
            self.YOUTUBE_API_KEYS.append(self.YOUTUBE_API_KEY)

        # Generate channels list
        with open(self.YOUTUBE_CHANNEL_LIST) as IDs:
            for id in json.load(IDs):
                urls.append(self.generate_channel_request(id))
        
        for url in urls:
            request = scrapy.Request(url=url, callback=self.parseChannel)
            request.meta['search_depth'] = 0
            yield request
    

    def parseChannel(self, response):
        '''
        method to handle the response for each Request made, response holds the page content (for web request)
        '''
        jsonresponse = json.loads(response.body) # change body to text, if encoding issues

        if not jsonresponse['items']:
            logging.info("Empty items in Channel Response.")
            return

        if not 'brandingSettings' in jsonresponse["items"][0]:
            logging.info("Missing item in Channel Response: brandingSettings {}".format(jsonresponse["items"][0]["id"]))
            return
        
        # crawl the related channels until max search depth is reached
        if response.meta['search_depth'] < self.MAX_SEARCH_DEPTH:
            if 'featuredChannelsUrls' in jsonresponse['items'][0]['brandingSettings']['channel']:
                for id in jsonresponse['items'][0]['brandingSettings']['channel']['featuredChannelsUrls']:
                    url = self.generate_channel_request(id)
                    request = scrapy.Request(url, callback=self.parseChannel)
                    request.meta['search_depth'] = response.meta['search_depth'] + 1
                    yield request


        id = jsonresponse["items"][0]["id"]
        title = jsonresponse["items"][0]["brandingSettings"]["channel"]["title"] if 'title' in jsonresponse["items"][0]["brandingSettings"]["channel"] else u'NO TITLE'
        keywords = quoteSplit(jsonresponse["items"][0]["brandingSettings"]["channel"]["keywords"]) if "keywords" in jsonresponse["items"][0]["brandingSettings"]["channel"] else []
        description = jsonresponse["items"][0]["brandingSettings"]["channel"]["description"] if "description" in jsonresponse["items"][0]["brandingSettings"]["channel"] else u''

        if not 'snippet' in jsonresponse["items"][0]:
            dateAdded = ''
        else:
            dateAdded = jsonresponse["items"][0]["snippet"]["publishedAt"] if "publishedAt" in jsonresponse["items"][0]["snippet"] else u''

        featuredChannelsIDs = jsonresponse['items'][0]['brandingSettings']['channel']['featuredChannelsUrls'] if 'featuredChannelsUrls' in jsonresponse['items'][0]['brandingSettings']['channel'] else []

        if not 'contentDetails' in jsonresponse["items"][0]:
            uploadsPlaylistID = ''
        else:
            uploadsPlaylistID = jsonresponse['items'][0]['contentDetails']['relatedPlaylists']['uploads'] if "uploads" in jsonresponse["items"][0]["contentDetails"]["relatedPlaylists"] else u''
        
        unsubscribedTrailer = jsonresponse['items'][0]['brandingSettings']['channel']['unsubscribedTrailer'] if 'unsubscribedTrailer' in jsonresponse['items'][0]['brandingSettings']['channel'] else u''

        if not 'topicDetails' in jsonresponse["items"][0]:
            topicIds = []
        else:
            topicIds = jsonresponse["items"][0]["topicDetails"]["topicIds"] if "topicIds" in jsonresponse["items"][0]["topicDetails"] else []

        # Channels constant infos
        yield ChannelItem(
                id = id,
                title = title,
                keywords = keywords,
                description = description,
                dateAdded = dateAdded,
                featuredChannelsIDs = featuredChannelsIDs,
                uploadsPlaylistID = uploadsPlaylistID,
                unsubscribedTrailer = unsubscribedTrailer,
                topicIds = topicIds,
                crawlTimestamp = time.strftime('%Y-%m-%d %H:%M:%S') 
            )

        if not 'contentDetails' in jsonresponse["items"][0]:
            logging.info("Missing item in Channel Response: contentDetails {}".format(jsonresponse["items"][0]["id"]))
            return
        
        # Get content of the uploads playlist (50 latest videos)
        playlistUrl = self.generate_playlistitems_request(jsonresponse['items'][0]['contentDetails']['relatedPlaylists']['uploads'])
        playlistRequest = scrapy.Request(playlistUrl, callback=self.parsePlaylist)
        playlistRequest.meta['channelID'] = jsonresponse["items"][0]["id"]
        yield playlistRequest


    def parsePlaylist(self, response):
        '''
        method to handle the response for each Request made, response holds the page content (for web request)
        '''
        jsonresponse = json.loads(response.body) # change body to text, if encoding issues

        if not jsonresponse['items']:
            logging.info("Empty items in Playlist Response {}".format(response.meta['channelID']))
            return
            
        videoList = []
        # crawl the playlistitems, videos in the list up to 50 entrys
        for video in jsonresponse['items']:
            videoList.append(video['contentDetails']['videoId'])

        yield VideoListItem(channelID=response.meta['channelID'], videoIDs=videoList)

        # Add videos to the database
        for video in videoList:
            request = scrapy.Request(url=self.generate_newvideo_request(video), callback=self.parseNewVideo)
            request.meta['videoID'] = video
            yield request

    def parseNewVideo(self, response):

        jsonresponse = json.loads(response.body) # change body to text, if encoding issues

        if not jsonresponse["items"]:
            logging.info("Empty video item response for new video:"+response.meta['videoID'])
            return

        if not 'snippet' in jsonresponse["items"][0] and not 'contentDetails' in jsonresponse["items"][0] and\
        not 'statistics' in jsonresponse["items"][0]:
            logging.info("Missing parts in video response for new video.")
            return

        if not 'topicDetails' in jsonresponse["items"][0]:
            topicIds = []
        else:
            topicIds = jsonresponse["items"][0]["topicDetails"]["topicIds"] if "topicIds" in jsonresponse["items"][0]["topicDetails"] else []

        # TODO check if diff method is really sufficient for new video filter
        # TODO check if parts present, set defaults else
        yield  VideoItem(
                id = jsonresponse["items"][0]["id"],
                channelID = jsonresponse["items"][0]["snippet"]["channelId"],
                title = jsonresponse["items"][0]["snippet"]["title"],
                description = jsonresponse["items"][0]["snippet"]["description"],
                category = jsonresponse['items'][0]['snippet']["categoryId"],
                duration = jsonresponse['items'][0]['contentDetails']["duration"],
                dateAdded = jsonresponse['items'][0]['snippet']["publishedAt"],
                tags = jsonresponse["items"][0]["snippet"]["tags"] if "tags" in jsonresponse["items"][0]["snippet"] else [],
                topicIds = topicIds,
                crawlTimestamp = time.strftime('%Y-%m-%d %H:%M:%S') 
            )

        yield  VideoStatisticsItem(
                id = jsonresponse["items"][0]["id"],
                viewCount = jsonresponse["items"][0]["statistics"]["viewCount"],
                commentCount = jsonresponse["items"][0]["statistics"]["commentCount"] if "commentCount" in jsonresponse["items"][0]["statistics"] else 0,
                likeCount = jsonresponse["items"][0]["statistics"]["likeCount"] if "likeCount" in jsonresponse["items"][0]["statistics"] else 0,
                dislikeCount = jsonresponse['items'][0]['statistics']["dislikeCount"] if "dislikeCount" in jsonresponse["items"][0]["statistics"] else 0,
                crawlTimestamp = time.strftime('%Y-%m-%d %H:%M:%S') 
            )
        

    def generate_channel_request(self, channelID):
        # costs: 11points
        return '{0}?key={1}&id={2}&part=brandingSettings,statistics,contentDetails,snippet,topicDetails&fields=items(id,statistics,topicDetails,snippet(publishedAt),brandingSettings(channel(title,description,keywords,featuredChannelsTitle,featuredChannelsUrls,unsubscribedTrailer)),contentDetails(relatedPlaylists(uploads)))'\
                .format(self.YOUTUBE_API_CHANNEL_URL, self.get_api_key(), channelID)

    def generate_playlistitems_request(self, playlistID):
        # costs: 3points
        # rather than search for videos in a certain time (1day here), grab the list of uploaded videos on first day, and every added video at the next day in the list is new
        # the playlistitems list is date order it seems, so in the first request should be the 50th newest videos
        return '{0}?key={1}&playlistId={2}&part=contentDetails&maxResults=50'\
                .format(self.YOUTUBE_API_PLAYLISTITEMS_URL, self.get_api_key(), playlistID)


    def generate_newvideo_request(self, videoID):
        # costs: ~9 points
        return '{0}?key={1}&id={2}&part=contentDetails,statistics,snippet,topicDetails&fields=items(id,statistics,topicDetails,contentDetails,snippet(publishedAt,channelId,title,tags,description,categoryId))'\
                .format(self.YOUTUBE_API_VIDEO_URL, self.get_api_key(), videoID)


    