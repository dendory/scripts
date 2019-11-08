#!/usr/bin/python3
# This script lists Wi-Fi signals nearby. It requires a Wi-Fi adapter to be connected.
# Also requires 'wireless-tools' to be installed

import os
import connix
from collections import OrderedDict

tmpfile = os.path.join("/tmp", connix.guid())
connix.cmd("sudo iwlist scan > {} 2> /dev/null".format(tmpfile))
with open(tmpfile, 'r') as fd:
	lines = fd.read().split('\n')

cell = None
ssid = {}
for line in lines:
	if "Cell" in line:
		cell = int(connix.in_tag(line, "Cell", "-"))
		ssid[cell] = {'essid': "", 'encryption': False, 'frequency': "", 'cipher': "", 'authentication': "", 'channel': "", 'MAC': line.split(': ')[1]}
	if cell:
		if "ESSID:" in line:
			ssid[cell]['essid'] = connix.in_tag(line, '"', '"')
		if "Frequency:" in line:
			ssid[cell]['frequency'] = connix.in_tag(line, ':', ' (')
			if ssid[cell]['frequency'] == "":
				ssid[cell]['frequency'] = line.split(':')[1]
		if "Channel:" in line:
			ssid[cell]['channel'] = int(line.split(':')[1])
		if "Encryption key:" in line:
			if line.split(':')[1] == "on":
				ssid[cell]['encryption'] = True
		if "Authentication Suites " in line:
			ssid[cell]['authentication'] = line.split(' : ')[1]
		if "Group Cipher " in line:
			ssid[cell]['cipher'] = line.split(' : ')[1]

o_ssid = OrderedDict(sorted(ssid.items(), key=lambda kv: kv[1]['channel']))
print("  # | Frequency | Cipher | Auth | MAC Address       | ESSID")
print("----+-----------+--------+------+-------------------+-------------------------------")
for k,s in o_ssid.items():
	print("{:3} | {:9} | {:6} | {:4} | {:17} | {:30}".format(s['channel'], s['frequency'], s['cipher'], s['authentication'], s['MAC'], s['essid']))

