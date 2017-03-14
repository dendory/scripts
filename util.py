#!/usr/bin/env python3
# Random utilities - (C) 2017 Patrick Lambert - http://dendory.net
# Provided under the MIT License

__VERSION__ = "2017.3.3"

import re
import os
import sys
import cgi
import time
import uuid
import json
import types
import string
import random
import fnmatch
import hashlib
import smtplib
import urllib.parse
import urllib.request

def guid(length=16):
	""" Return a unique ID based on the machine, current time in milliseconds, and random number.
			@param length: The length of the ID (optional, defaults to 16 bytes)
	"""
	hw = str(hex(uuid.getnode() + int(time.time()*1000000)))[2:]
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

def now(timestamp=time.gmtime()):
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
	import cgitb
	cgitb.enable(context=1)
	result = {}
	form = cgi.FieldStorage()
	for key in form.keys():
		result[key] = form.getvalue(key)
	return result

def header(content_type="text/html", filename=None):
	""" Return the header needed for a CGI application.
			@param content_type: The type of content delivered (optional, defaults to text/html)
			@param filename: Set the content to be a downloadable file (optional)
	"""
	output = "Content-Type: " + str(content_type) + "; charset=utf-8\n\n"
	if filename:
		output = "Content-Disposition: attachment; filename=" + filename + "\n" + output
	return output

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

def curl(url, encoding="utf8", cookie=None):
	""" Get the content of a URL.
			@param url: The URL to query
			@param encoding: The decoding format (optional, defaults to UTF-8)
			@param cookie: The cookie string in format key1=value1;key2=value2 (optional)
	"""
	if cookie:
		headers = {
			'Cookie': cookie,
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
		}
	else:
		headers = {
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
		}
	con = urllib.request.Request(url, headers=headers)
	stream = urllib.request.urlopen(con)
	result = stream.read()
	charset = stream.info().get_param('charset', encoding)
	return result.decode(charset)

def download(url, localfile):
	""" Download a file from the Internet.
			@param url: The url of the file
			@param localfile: Where to save that file
	"""
	urllib.request.urlretrieve(url, localfile)
	return os.stat(localfile).st_size

def in_list(ldict, key, value):
	""" Find whether a key/value pair is inside of a list of dictionaries.
			@param ldict: List of dictionaries
			@param key: The key to use for comparision
			@param value: The value to look for
	"""
	for l in ldict:
		if l[key] == value:
			return True
	return False

def remove_spaces(text):
	""" Remove extra spaces from a string.
			@param text: The string to process
	"""
	return re.sub("\s\s+", " ", text).strip()

def cmd(command):
	""" Run a command and return the output.
			@param command: The command to run
	"""
	return os.popen(command).read().rstrip('\n')

def ask(question, default=""):
	""" Ask a question with a default answer.
			@param question: The question to ask
			@param default: The default answer (optional)
	"""
	tmp = input(question + " [" + str(default) + "]: ")
	if tmp == "":
		return default
	return tmp

def alphanum(text, symbols=False, spaces=False):
	""" Return only letters, numbers and optionally basic symbols and spaces in a string.
			@param text: The string to process
			@param symbols: Whether to leave basic symbols
			@param spaces: Whether to leave spaces
	"""
	if spaces and symbols:
		return re.sub('[^0-9a-zA-Z \_\-\.\[\]\(\)\@\!\?\:\'\;]+', '', text)
	elif spaces:
		return re.sub('[^0-9a-zA-Z ]+', '', text)
	elif symbols:
		return re.sub('[^0-9a-zA-Z\_\-\.\[\]\(\)\@\!\?\:\'\;]+', '', text)
	return re.sub('[^0-9a-zA-Z]+', '', text)

def list_files(folder, pattern="*"):
	""" Return a list of files in a folder recursively.
			@param folder: The folder to list files from
			@param pattern: The pattern files must match (optional)
	"""
	matches = []
	for root, dirnames, filenames in os.walk(folder):
		for filename in fnmatch.filter(filenames, pattern):
			matches.append(os.path.join(root, filename))
	return matches





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
	_test("now", [])
	_test("hashfile", [jsonfile])
	_test("hashfile", ["/doesnotexist"])
	_test("error", [])
	_test("hash", ["Hello world"])
	_test("remote_ip", [])
	_test("form", [])
	_test("email", ["root@localhost", "root@localhost", "Test 1 2 3", "This is\na\ntest!"])
	_test("curl", ["http://google.com/does.not.exist"])
	_test("in_list", [[{'id': "1", 'text': "Hello world"}, {'id': "2", 'text': "World hello"}, {'id': "3", 'text': "!"}], "id", "4"])
	_test("remove_spaces", ["  This is  a test of   the \"emergency  broadcast system\". "])
	_test("cmd", ["ps aux | wc -l"])
	saveto = "/tmp/" + guid() + ".html"
	_test("download", ["http://www.cnn.com", saveto])
	_test("alphanum", ["Some escape attempt\"); cat /etc/passwd", True, True])
	_test("list_files", ["/etc/httpd", "*.conf"])
	_test("ask", ["Type something", "nothing"])
