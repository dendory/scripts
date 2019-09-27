#!/usr/bin/env python3
# This script gets weather information from Canada Weather Service about a city (Montreal by default) and displays it as a web page.

import os
import sys
import time
import connix
import feedparser
import re

rss = feedparser.parse("https://weather.gc.ca/rss/city/qc-147_e.xml")

print(connix.header())

print("<html><head><link href='/bootstrap.min.css' rel='stylesheet' /><link href='https://use.fontawesome.com/releases/v5.8.1/css/all.css' rel='stylesheet' /><style>body{background-color:#000000;color:#FFFFFF;font-family:Verdana;}*{font-size:24px!important;}</style></head><body>")

def get_temp(t):
#   return re.sub('[^\d.]+', '', str(t))
    return str(t).split(':')[1]

def get_icon(a):
    icon = "<i class='fa fa-question'></i>"

    if "rain" in str(a).lower():
        icon = "<i class='fa fa-cloud-rain'></i>"
    elif "shower" in str(a).lower():
        icon = "<i class='fa fa-cloud-showers-heavy'></i>"
    elif "cloud" in str(a).lower():
        icon = "<i class='fa fa-cloud'></i>"
    elif "snow" in str(a).lower():
        icon = "<i class='fa fa-snow'></i>"
    elif "sun" in str(a).lower():
        icon = "<i class='fa fa-sun'></i>"
    elif "clear" in str(a).lower():
        icon = "<i class='fa fa-cloud-sun'></i>"

    return icon

print("<table class='table table-bordered'>")
print("<tr><td><b>Currently:</b></td><td>{} {}</td></tr>".format(get_icon(rss['items'][1]['title']), get_temp(rss['items'][1]['title'])))
print("<tr><td><b>{}:</b></td><td>{} {}</td></tr>".format(str(rss['items'][2]['title']).split(':')[0], get_icon(rss['items'][2]['title']), get_temp(rss['items'][2]['title'])))
print("<tr><td><b>{}:</b></td><td>{} {}</td></tr>".format(str(rss['items'][3]['title']).split(':')[0], get_icon(rss['items'][3]['title']), get_temp(rss['items'][3]['title'])))
print("<tr><td><b>{}:</b></td><td>{} {}</td></tr>".format(str(rss['items'][4]['title']).split(':')[0], get_icon(rss['items'][4]['title']), get_temp(rss['items'][4]['title'])))
print("<tr><td><b>{}:</b></td><td>{} {}</td></tr>".format(str(rss['items'][5]['title']).split(':')[0], get_icon(rss['items'][5]['title']), get_temp(rss['items'][5]['title'])))
print("<tr><td><b>{}:</b></td><td>{} {}</td></tr>".format(str(rss['items'][6]['title']).split(':')[0], get_icon(rss['items'][6]['title']), get_temp(rss['items'][6]['title'])))
print("</table>")





