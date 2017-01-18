#!/usr/bin/env python3
# Line RePlace - (C) 2017 Patrick Lambert - http://dendory.net
# Provided under the MIT License

import sys

if len(sys.argv) != 4 and len(sys.argv) != 5:
	print("Line RePlace - Look for a tag in a file, and replace that line with a replacement text")
	print("Syntax: " + sys.argv[0] + " <filename> <tag> <replacement text> [section]")
	quit(1)

file = sys.argv[1]
tag = sys.argv[2]
text = sys.argv[3]
section = False
if len(sys.argv) > 4:
	section = sys.argv[4]

try:
	with open(file, 'r') as fd:
		data = fd.read()
except:
	print("Error: Could not read from " + file + ".")
	quit(1)

results = []
tag_found = False
section_found = False

for line in data.split('\n'):
	if tag in line and (section_found or not section) and (not section or not tag_found) and len(line) > 1 and line[0] != "#":
		line = text
		tag_found = True
	if section and section in line:
		section_found = True
	results.append(line)

try:
	with open(file, 'w') as fd:
		for result in results:
			fd.write(result + "\n")
			if not tag_found and section and section in result:
				fd.write(text + "\n")
		if not tag_found and not section:
			fd.write(text + "\n")
except:
	print("Error: Could not write to " + file + ".")
	quit(1)

quit(0)

