#!/usr/bin/env python

import subprocess
import os

# copy src directory to the pi
p = subprocess.Popen(['scp', '-r', './src/', 'pi@natePi.local:/home/pi/Documents/enee408a'])
sts = os.waitpid(p.pid, 0)
print('Uploaded new src to pi')
# tell it to run the ampy command to copy src to the esp8266 chip
p = subprocess.Popen(['ssh','pi@natePi.local', 'cd /home/pi/Documents/enee408a; ./update.bash'])
sts = os.waitpid(p.pid, 0)
print('Pushed src onto the esp chip')
