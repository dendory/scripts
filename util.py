#!/usr/bin/env python3
# Random utilities - (C) 2017 Patrick Lambert - http://dendory.net
# Provided under the MIT License

__VERSION__ = "2"

import os
import sys
import cgi
import time
import uuid
import json
import types
import string
import random
import hashlib
import smtplib
import urllib.parse
import urllib.request

def guid(length=16):
	""" Return a unique ID based on the machine, current time in milliseconds, and random number.
			@param length: The length of the ID (optional, defaults to 16 bytes)
	"""
	hw = str(hex(uuid.getnode() + int(time.time()*1000)))[2:]
	pad = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(length-len(hw)))
	return str(hw + pad).upper()

def in_tag(text, first, last=None):
	""" Return what's between the first occurrence of 2 unique tags, or in between an HTML tag.
			@param text: The text to evaluate
			@param first: The first tag
			@param last: The last tag (optional, takes the first as a closing HTML tag otherwise)
	"""
	try:
		if last:
			start = text.index(first) + len(first)
			tmp = text[start:]
			end = tmp.index(last)
			result = tmp[:end]
		else:
			last = "</" + first + ">"
			first = "<" + first
			start = text.index(first) + len(first)
			tmp = text[start:]
			start = tmp.index(">") + 1
			end = tmp.index(last, start)
			result = tmp[start:end]
		return result.replace('\n','').replace('\r','').strip()
	except ValueError:
		return ""

def load(filename):
	""" Load a JSON file.
			@param filename: The filename to load from
	"""
	with open(filename, 'r') as fd:
		data = fd.read()
	return json.loads(data)

def save(filename, data):
	""" Save data in a JSON file.
			@param filename: The filename to use
			@param data: The object to save
	"""
	with open(filename, 'w') as fd:
		fd.write(json.dumps(data, sort_keys = False, indent = 4))

def unixtime():
	""" Return the current UTC time in seconds.
	"""
	return int(time.time())

def datetime(timestamp=time.gmtime()):
	""" Return the current UTC date and time in a standard format.
			@param timestamp: The time object to use (optional)
	"""
	return time.strftime("%Y-%m-%d %H:%M:%S", timestamp)

def hashfile(filename):
	""" Return a unique hash for the content of a file.
			@param filename: The file to hash.
	"""
	BLOCKSIZE = 65536
	hasher = hashlib.sha256()
	with open(filename, "rb") as fd:
		buf = fd.read(BLOCKSIZE)
		while len(buf) > 0:
			hasher.update(buf)
			buf = fd.read(BLOCKSIZE)
	return str(hasher.hexdigest()).upper()

def hash(text):
	""" Return a unique hash for a string.
			@param text: The string to hash
	"""
	hasher = hashlib.sha256(text.encode())
	return str(hasher.hexdigest()).upper()

def remote_ip():
	""" Return the remote IP of a CGI application.
	"""
	if "REMOTE_ADDR" in os.environ:
		return str(cgi.escape(os.environ['REMOTE_ADDR']))
	return ""

def form():
	""" Return the GET and POST variables in a CGI application.
	"""
	result = {}
	form = cgi.FieldStorage()
	for key in form.keys():
		result[key] = form.getvalue(key)
	return result

def header(content_type="text/html"):
	""" Return the header needed for a CGI application.
			@param content_type: The type of content delivered (optional, defaults to text/html)
	"""
	return "Content-Type: " + str(content_type) + "; charset=utf-8\n\n"

def error():
	""" Return the error message after an exception. Must be used in an 'except' statement.
	"""
	a, b, c = sys.exc_info()
	return str(b)

def email(fromaddr, toaddr, subject, body):
	""" This will send an email.
			@param fromaddr: Email of sender
			@param toaddr: Email of recipient
			@param subject: Subject of the email
			@param body: Body of the email
	"""
	smtpObj = smtplib.SMTP("localhost")
	smtpObj.sendmail(str(fromaddr), str(toaddr), "From: " + str(fromaddr) + "\nTo: " + str(toaddr) +"\nSubject: " + str(subject).replace('\n','').replace('\r','') + "\n\n" + str(body) + "\n")

def curl(url):
	""" Get the content of a URL.
			@param url: The URL to query
	"""
	stream = urllib.request.urlopen(url)
	result = stream.read()
	charset = stream.info().get_param('charset', 'utf8')
	return result.decode(charset)

def in_list(ldict, key, value):
	"""Find whether a key/value pair is inside of a list of dictionaries.
			@param ldict: List of dictionaries
			@param key: The key to use for comparision
			@param value: The value to look for
	"""
	if next((i for i, item in enumerate(ldict) if item[key] == value), -1) > 0:
		return True
	return False






def _test(func, args):
	""" Test a function with optional arguments.
	"""
	possibles = globals().copy()
	print("* util." + func + "(" + str(args)[1:-1] + ")")
	method = possibles.get(func)
	#print(method.__doc__)
	try:
		print(method(*args))
	except:
		print(error())
	print()

if __name__ == '__main__':
	""" If called directly, run through a number of sanity tests.
	"""
	print("Python3 util module v" + __VERSION__ + " by Patrick Lambert")
	print("Testing functions...")
	print()
	_test("guid", [])
	_test("guid", [32])
	_test("in_tag", ["this random string is something, right?", "random", ","])
	_test("in_tag", ["<p>This is a link to <a href='http://google.com'>Google</a>.</p>", "a"])
	jsonfile = "/tmp/" + guid() + ".json"
	data = {'name': "Hello world", 'results': ["test 1", "test 2", "test 3"]}
	_test("save", [jsonfile, data])
	_test("load", [jsonfile])
	_test("unixtime", [])
	_test("datetime", [])
	_test("hashfile", [jsonfile])
	_test("hashfile", ["/doesnotexist"])
	_test("error", [])
	_test("hash", ["Hello world"])
	_test("remote_ip", [])
	_test("form", [])
	_test("email", ["root@localhost", "root@localhost", "Test 1 2 3", "This is\na\ntest!"])
	_test("curl", ["http://google.com/does.not.exist"])
	_test("in_list", [[{'id': "1", 'text': "Hello world"}, {'id': "2", 'text': "World hello"}, {'id': "3", 'text': "!"}], "id", "4"])
