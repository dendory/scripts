#!/usr/bin/python3
# This script will request X number of random users and create users based on that data
number_of_users = "20"

import urllib.request
import urllib.parse
import json
import os

stream = urllib.request.urlopen("https://randomuser.me/api/?results=" + number_of_users)
users = json.loads(stream.read().decode("utf-8"))
for u in users['results']:
	print("Creating user " + u['login']['username'] + " (" + u['name']['first'] + " " + u['name']['last'] + ")")
	print(os.popen("useradd -c '" + u['name']['first'] + " " + u['name']['last'] + "' " + u['login']['username']).read())
	print(os.popen("echo " + u['login']['username'] + ":" + u['login']['password'] + " | chpasswd").read())
