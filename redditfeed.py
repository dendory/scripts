#!/usr/bin/env python3
# This script will keep running and fetch news from the configured subreddits, showing new entries every 30 secs.

import os
import sys
import time
import connix
import feedparser

feeds = ["sysadmin", "worldnews", "pcmasterrace", "netsec"]

try:
	old = connix.load("redditfeed.json")
except:
	old = []

while True:
	for feed in feeds:
		rss = feedparser.parse("https://www.reddit.com/r/{}/.rss".format(feed))
		for item in rss['items']:
			if item['link'] not in old:
				print("[{}] {} {}".format(connix.bold(item['updated'].replace('T',' ').split('+')[0]), item['title'], connix.underline(item['link'])))
				old.append(item['link'])

	connix.save("redditfeed.json", old)
	time.sleep(30)
