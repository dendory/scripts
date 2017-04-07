#!/usr/local/bin/python3
#
# This will backup all master branches of the following GitHub user:
user = "dendory"
target_file = "/storage/backups/github_backup.tgz"

import connix as util
import json
import os

repos = json.loads(util.curl("https://api.github.com/users/" + user + "/repos"))
os.system("mkdir /tmp/github")

for repo in repos:
	if not repo["fork"]:
		print(str(repo["name"]))
		os.system("cd /tmp/github && wget -q https://github.com/" + repo["full_name"] + "/archive/master.zip && mv master.zip " + repo["name"] + ".zip")

os.system("cd /tmp && tar czf " + target_file + " github")
os.system("rm -rf /tmp/github")
