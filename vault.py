#!/usr/bin/python3
#
# This script allows the storage of secrets in an encrypted vault
# Created by Patrick Lambert - http://dendory.net

import os
import connix
import getpass
from operator import itemgetter

# Get master key and vault file
key = getpass.getpass("Master key: ")
vaultfile = os.path.join(os.path.expanduser("~"), ".vault")
entries = []

# Create vault file if it doesn't exist
try:
	entries = connix.load(vaultfile)
except:
	print("* Empty vault, creating new file.")
	entries.append({'type': "verify", 'name': "_verify", 'secret': connix.encrypt(key, "verify")})
	connix.save(vaultfile, entries)

os.chmod(vaultfile, 0o600)
filter = ""

# Check if the master password is correct
for entry in sorted(entries, key=itemgetter('name')):
	if entry['type'] == "verify":
		try:
			if connix.decrypt(key, entry['secret']) != "verify":
				print("ERROR - Invalid master key.")
				quit(1)
		except:
			print("ERROR - Invalid master key.")
			quit(1)

# Main loop
while True:
	print()
	i = 0
	for entry in sorted(entries, key=itemgetter('name')):
		if filter.lower() in entry['name'].lower() and entry['type'] != "verify":
			print(str(i) + ": " + entry['name'] + " (" + entry['login'] + ")")
		i = i + 1
	filter = ""
	r = connix.ask("Enter an entry ID, <ENTER> to create a new entry, or <Q> to quit")
	if r.lower() == 'q':
		print("* Saving vault.")
		connix.save(vaultfile, entries)
		print("* Exiting.")
		quit()
	elif r == "":
		print("* Creating new entry.")
		name = connix.ask("Name:")
		if name != "":
			login = connix.ask("Login:")
			found = False
			for e in entries:
				if e['name'].lower() == name.lower() and e['login'].lower() == login.lower():
					if not found:
						print("* Name and login already exist, aborting.")
					found = True
			if not found:
				type = "login"
				secret = "1"
				confirm = "2"
				while secret != confirm:
					secret = getpass.getpass("Secret: ")
					confirm = getpass.getpass("Confirm secret: ")
					if secret != confirm:
						print("Mismatch!")
				note = connix.ask("Note:")
				newentry = {'name': name, 'login': login, 'secret': connix.encrypt(key, secret), 'note': note, 'type': type}
				entries.append(newentry)
				print("* Added.")
	elif connix.is_int(r):
		i = 0
		for entry in sorted(entries, key=itemgetter('name')):
			if i == int(r):
				while True:
					print()
					print("* " + entry['name'])
					print("Login: " + entry['login'])
					entryok = True
					print("Secret: " + '*' * len(connix.decrypt(key, entry['secret'])))
					print("Note: " + entry['note'])
					z = connix.ask("Press <E> to edit the entry, <V> to view the secret, <D> to delete it, <ENTER> to go back")
					if z.lower() == 'q' or z == '':
						break
					if z.lower() == 'v':
						print(connix.decrypt(key, entry['secret']))
					if z.lower() == 'd':
						print("* Removing entry")
						entries.remove(entry)
						break
					if z.lower() == 'e' and entryok:
						entry['login'] = connix.ask("Login", entry['login'])
						secret = "1"
						confirm = "2"
						while secret != confirm:
							secret = getpass.getpass("Secret [" + '*' * len(connix.decrypt(key, entry['secret'])) + "]: ")
							confirm = getpass.getpass("Confirm secret [" + '*' * len(connix.decrypt(key, entry['secret'])) + "]: ")
							if secret != confirm:
								print("Mismatch!")
						if secret != "":
							entry['secret'] = connix.encrypt(key, secret)
						entry['note'] = connix.ask("Note", entry['note'])
			i = i + 1
	else:
		filter = r


