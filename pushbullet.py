# Python unofficial Pushbullet client
# (C) 2015 Patrick Lambert - http://dendory.net - Provided under MIT License
import urllib.request
import sys

api_key = "XXXXXXXXX"
title = "My Title"
message = "My Body"

def notify(key, title, text):
	post_params = {
		'type': 'note',
		'title': title,
		'body': text
	}
	post_args = urllib.parse.urlencode(post_params)
	data = post_args.encode()
	request = urllib.request.Request(url='https://api.pushbullet.com/v2/pushes', headers={'Authorization': 'Bearer ' + key}, data=data)
	result = urllib.request.urlopen(request)
	return result.read().decode('utf-8')

if '-key' in sys.argv:
	api_key = sys.argv[sys.argv.index('-key')+1]
if '-title' in sys.argv:
	title = sys.argv[sys.argv.index('-title')+1]
if '-message' in sys.argv:
	message = sys.argv[sys.argv.index('-message')+1]

print(notify(api_key, title, message))
