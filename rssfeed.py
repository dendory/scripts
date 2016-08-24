#!/usr/bin/env python3
# Converts a RSS feed into an HTML output
import feedparser

print("HTTP/1.0 200 OK")
print("Content-Type: text/html; charset=utf-8")
print()
feed = feedparser.parse("http://www.ctvnews.ca/rss/ctvnews-ca-world-public-rss-1.822289")
print("<html><head><meta http-equiv='REFRESH' content='30;url=feed1.py'><style>body{background-color:#000000;color:#FFFFFF;font-family:Verdana;}.desc{font-size:22px;vertical-align:text-top;}.title{font-size:32px;}a{color:cyan;}</style><head><body>")
print("<a href='" + feed["items"][0]["link"] + "'><b class='title'>" + feed["items"][0]["title"] + "</b></a><br>")
print("<table class='desc'><tr>")
try:
	 print("<td style='vertical-align:top'><img src='" + feed["items"][0]['links'][1]['url'] + "'></td>")
except:
	 pass
print("<td>" + feed["items"][0]["description"] + "</td></table><br>")
print("<a href='" + feed["items"][1]["link"] + "'><b class='title'>" + feed["items"][1]["title"] + "</b></a><br>")
print("<table class='desc'><tr>")
try:
	 print("<td style='vertical-align:top'><img src='" + feed["items"][1]['links'][1]['url'] + "'></td>")
except:
	 pass
print("<td>" + feed["items"][1]["description"] + "</td></table><br>")
print("<a href='" + feed["items"][2]["link"] + "'><b class='title'>" + feed["items"][2]["title"] + "</b></a><br>")
print("<table class='desc'><tr>")
try:
	 print("<td style='vertical-align:top'><img src='" + feed["items"][2]['links'][1]['url'] + "'></td>")
except:
	 pass
print("<td>" + feed["items"][2]["description"] + "</td></table><br>")
print("</body></html>")
