#!/usr/bin/python3

import os
import connix
import getpass
from operator import itemgetter

key = getpass.getpass("Master key: ")
vaultfile = os.path.join(os.path.expanduser("~"), ".vault")
entries = []

try:
	entries = connix.load(vaultfile)
except:
	print("* Empty vault, creating new file.")
	connix.save(vaultfile, entries)

os.chmod(vaultfile, 0o600)

while True:
	print()
	i = 0
	for entry in sorted(entries, key=itemgetter('name')):
		print(str(i) + ": " + entry['name'] + " (" + entry['login'] + ")")
		i = i + 1
	r = connix.ask("Enter an entry ID, <ENTER> to create a new entry, or <Q> to quit")
	if r.lower() == 'q':
		print("* Saving vault.")
		connix.save(vaultfile, entries)
		print("* Exiting.")
		quit()
	if r == "":
		print("* Creating new entry.")
		name = connix.ask("Name:")
		found = False
		for e in entries:
			if e['name'].lower() == name.lower() or name == "":
				if not found:
					print("* Name is empty or already exists, aborting.")
				found = True
		if not found:
			login = connix.ask("Login:")
			secret = connix.ask("Secret:")
			note = connix.ask("Note:")
			newentry = {'name': name, 'login': login, 'secret': connix.encrypt(key, secret), 'note': note}
			entries.append(newentry)
			print("* Added.")
	if connix.is_int(r):
		i = 0
		for entry in sorted(entries, key=itemgetter('name')):
			if i == int(r):
				while True:
					print("* " + entry['name'])
					print("Login: " + entry['login'])
					entryok = True
					try:
						print("Secret: " + connix.decrypt(key, entry['secret']))
					except:
						entryok = False
						print("Secret: ERROR - Invalid master key")
					print("Note: " + entry['note'])
					if entryok:
						z = connix.ask("Press <E> to edit the entry, <D> to delete it, <ENTER> to go back")
					else:
						z = connix.ask("Press <D> to delete the entry, <ENTER> to go back")
					if z.lower() == 'q' or z == '':
						break
					if z.lower() == 'd':
						print("* Removing entry")
						entries.remove(entry)
						break
					if z.lower() == 'e' and entryok:
						entry['login'] = connix.ask("Login", entry['login'])
						entry['secret'] = connix.encrypt(key, connix.ask("Secret", connix.decrypt(key, entry['secret'])))
						entry['note'] = connix.ask("Note", entry['note'])
			i = i + 1


