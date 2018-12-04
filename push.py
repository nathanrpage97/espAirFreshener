#!/usr/bin/env python

import subprocess
import os

# copy src directory to the pi
p = subprocess.Popen(['scp', '-r', './src/', 'pi@natePi.local:/home/pi/Documents/enee408a'])
sts = os.waitpid(p.pid, 0)
print('Uploaded new src to pi')
