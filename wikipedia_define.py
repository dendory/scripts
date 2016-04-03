#!/usr/bin/env python3
# Uses the wikipedia module to define words on the command line

import wikipedia
import sys

sys.argv.pop(0)

for word in sys.argv:
	try:
		if word[0] != '-':
			if '-full' in sys.argv:
				print(wikipedia.summary(word))
			else:
				print(wikipedia.summary(word, sentences=1))
	except:
		print("* Unknown word: " + word)

