#!/usr/local/bin/python3
#
# This will backup all master branches of the following GitHub user:
user = "dendory"
target_file = "~/github_backup.tgz"

import os
import json
import urllib.parse
import urllib.request

stream = urllib.request.urlopen("https://api.github.com/users/" + user + "/repos")
result = stream.read()
charset = stream.info().get_param('charset', 'utf8')
repos = json.loads(result.decode(charset))

os.system("mkdir /tmp/github")
for repo in repos:
	os.system("cd /tmp/github && wget https://github.com/" + repo["full_name"] + "/archive/master.zip && mv master.zip " + repo["name"] + ".zip"")
os.system("cd /tmp && tar czf " + target_file + " github")
os.system("rm -rf /tmp/github")

