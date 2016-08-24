#!/usr/bin/env python3
# This script will play a number of mp3 files in random order

from random import shuffle
from subprocess import call
files = ['1.mp3', '2.mp3', '3.mp3', '4.mp3', '5.mp3', '6.mp3', '7.mp3', '8.mp3']
shuffle(files)
for file in files:
    call(["omxplayer", file])
