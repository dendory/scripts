#!/usr/local/python3.6/bin/python3.6
#
# This is a very simple script which allows you to start and stop music
# from the iOS HomeKit app. Simply start this script from the command
# line once, register the device with the on-screen code on your iOS
# device, then you can start this script on bootup for next time.
#
# Usage: $ python3 ./pi_playlist.py /my/music/folder/here
#
# Requirements: Python 3.3+, HAP-Python, OMXPlayer
#
# Created by: Patrick Lambert (https://dendory.net)
#

import os
import sys
import signal
from random import shuffle
import pyhap.loader as loader
from pyhap.accessory_driver import AccessoryDriver
from pyhap.accessory import Accessory, Category

class PiPlaylist(Accessory):

	category = Category.SWITCH
	music_folder = "/home/pi/music"

	def __init__(self, *args, **kwargs):
		super(PiPlaylist, self).__init__(*args, **kwargs)
		self.music = self.get_service("Switch").get_characteristic("On")
		self.music.setter_callback = self.set_music
		self.t = None

	def _set_services(self):
		super(PiPlaylist, self)._set_services()
		service_loader = loader.get_serv_loader()
		switch = service_loader.get("Switch")
		self.add_service(switch)

	def run(self):
		print("Accessory running.")
		self.set_music_state(0)

	def stop(self):
		print("Stopping accessory...")
		self.set_music_state(0)

	def set_music(self, state):
		self.set_music_state(state)

	def music_worker(self):
		files = os.listdir(self.music_folder)
		shuffle(files)
		for file in files:
			call(["omxplayer", os.path.join(self.music_folder, file)])

	def set_music_state(self, state):
		if int(state) == 1:
			print("Starting music in [{}]...".format(self.music_folder))
			files = os.listdir(self.music_folder)
			shuffle(files)
			with open("/tmp/pi_player.sh", "w") as fd:
				fd.write("#!/bin/bash\n")
				for file in files:
					fd.write("echo '1' > /tmp/fifo\n")
					fd.write("omxplayer {} < /tmp/fifo\n".format(os.path.join(self.music_folder, file)))
			os.popen("chmod 777 /tmp/pi_player.sh")
			os.popen("/tmp/pi_player.sh &")
		else:
			print("Stopping all music...")
			os.popen("killall -9 -q pi_player.sh")
			os.popen("killall -9 -q omxplayer.bin")

	def next_track(self):
		print("Next track...")
		os.popen("killall -9 -q omxplayer.bin")


print("Starting Pi Playlist...")
playlist = PiPlaylist("Pi Playlist")

driver = AccessoryDriver(playlist, port=51826)

paired_devices = []
for k,v in playlist.paired_clients.items():
	paired_devices.append(k)

if len(sys.argv) > 1:
	if sys.argv[1] == "-unpair":
		print("Removing paired devices...")
		for p in paired_devices:
			playlist.remove_paired_client(p)
	else:
		playlist.music_folder = sys.argv[1]

for p in paired_devices:
	print("Paired with: {}".format(p))

signal.signal(signal.SIGINT, driver.signal_handler)
signal.signal(signal.SIGTERM, driver.signal_handler)
driver.start()

