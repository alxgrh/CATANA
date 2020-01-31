#!/bin/bash

PATH=$PATH:/usr/bin
export PATH

# change path here for user
cd /catana/src/data_collection/youtubeAPICrawler/

scrapy crawl update
