#!/usr/bin/env python3
""" Connix is a general purpose Python 3.x library that contains a lot of commonly done operations inside of a single package.
    (C) 2018 Patrick Lambert - http://dendory.net - Provided under the MIT License
"""

__VERSION__ = "1.16"

import re
import os
import sys
import cgi
import time
import uuid
import json
import types
import base64
import string
import random
import fnmatch
import hashlib
import smtplib
import logging
import inspect
import datetime
import urllib.parse
import urllib.request
from http.cookiejar import CookieJar

def logger(file):
	""" Return a logger with sensible defaults.
			@param file: Filename where to log
	"""
	logging.basicConfig(filename = file, level = logging.INFO, format = "{} - %(levelname)s - %(asctime)s - %(message)s".format(inspect.getframeinfo(inspect.getouterframes(inspect.currentframe())[1][0])[0]))
	return logging.getLogger()

def urlencode(text):
	""" Encode text for use on a URL bar.
			@param text: The text to encode
	"""
	return urllib.parse.quote_plus(text)

def max_len(text, max):
	""" Return a string capped at a specific length.
			@param text: The text to return
			@param max: The maximum length of the string
	"""
	return text if len(text)<=max else text[0:max-3]+'...'

def encrypt(key, text):
	""" Return an AES encrypted version of the text.
			@param key: The key to use for the encryption
			@param text: The string to encrypt
	"""
	from Crypto import Random
	from Crypto.Cipher import AES
	text = text + (32 - len(text) % 32) * chr(32 - len(text) % 32)
	iv = Random.new().read(AES.block_size)
	rawkey = hashlib.sha256(key.encode()).digest()
	cipher = AES.new(rawkey, AES.MODE_CBC, iv)
	return base64.b64encode(iv + cipher.encrypt(text)).decode('utf-8')

def decrypt(key, text):
	""" Return the plain text version of an encrypted string.
			@param key: The key used for the encryption
			@param text: The cipher text to decrypt
	"""
	from Crypto import Random
	from Crypto.Cipher import AES
	enc = base64.b64decode(text.encode())
	iv = enc[:AES.block_size]
	rawkey = hashlib.sha256(key.encode()).digest()
	cipher = AES.new(rawkey, AES.MODE_CBC, iv)
	result = cipher.decrypt(enc[AES.block_size:])
	result = result[:-ord(result[len(result)-1:])]
	return result.decode('utf-8')

def remove_tags(text):
	""" Return the text without any HTML tags in it.
			@param text: The text to process
	"""
	return re.sub('<[^<]+?>', '', text)

def bold(text):
	""" Return the text in bold (Linux console only).
			@param text: The text to bold
	"""
	return "\033[1m" + str(text) + "\033[0m"

def underline(text):
	""" Return the text in underline (Linux console only).
			@param text: The text to underline
	"""
	return "\033[4m" + str(text) + "\033[0m"

def is_int(number):
	""" Check if a variable can be cast as an int.
			@param number: The number to check
	"""
	try:
		x = int(number)
		return True
	except:
		return False

def is_float(number):
	""" Check if a variable can be cast as a floating point.
			@param number: The number to check
	"""
	try:
		x = float(number)
		return True
	except:
		return False

def base36(number):
	""" Converts an integer to an alphanumeric string.
			@param number: The number to convert
	"""
	base36 = ""
	alphabet = string.digits + string.ascii_uppercase

	while int(number) > 0:
		number, i = divmod(int(number), len(alphabet))
		base36 = alphabet[i] + base36

	return base36

def guid(length=16):
	""" Return a unique ID based on the machine, current time in milliseconds, and random number.
			@param length: The length of the ID (optional, defaults to 16 bytes)
	"""
	hw = str(base36(uuid.getnode() + int(time.time()*1000000)))
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

def args(format="dict"):
	""" Return the arguments passed to the script, divided by spaces or dashes.
			@param format: Whether to return as a space separated string or as a dash separated dict
	"""
	p = ""
	sys.argv.pop(0)
	for arg in sys.argv:
		p += arg + " "
	if format.lower() != "dict":
		if len(p) > 0:
			return p[:-1]
		else:
			return p
	else:
		d = []
		if len(p) > 0:
			p = " " + p[:-1]
			for arg in p.split(' -'):
				d.append("-" + arg)
			d.pop(0)
		return d

def load(filename):
	""" Load a JSON file.
			@param filename: The filename to load from
	"""
	with open(filename, 'r', encoding='UTF-8') as fd:
		data = fd.read()
	return json.loads(data)

def save(filename, data):
	""" Save data in a JSON file.
			@param filename: The filename to use
			@param data: The object to save
	"""
	with open(filename, 'w', encoding='UTF-8') as fd:
		fd.write(json.dumps(data, sort_keys = False, indent = 4))

def unixtime():
	""" Return the current UTC time in seconds.
	"""
	return int(time.time())

def unixtime2datetime(unixtime):
	""" Convert unixtime to a date/time string.
			@param unixtime: A numeric unixtime value
	"""
	return datetime.datetime.fromtimestamp(int(unixtime)).strftime('%Y-%m-%d %H:%M:%S')

def now():
	""" Return the current UTC date and time in a standard format.
	"""
	return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

def hashfile(filename):
	""" Return a unique hash for the content of a file.
			@param filename: The file to hash
	"""
	BLOCKSIZE = 65536
	hasher = hashlib.sha256()
	with open(filename, "rb", encoding='UTF-8') as fd:
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
	cj = CookieJar()
	opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
	stream = opener.open(con)
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
	print("* connix." + func + "(" + str(args)[1:-1] + ")")
	method = possibles.get(func)
	#print(method.__doc__)
	try:
		print(method(*args))
	except:
		print(error())
	print()
