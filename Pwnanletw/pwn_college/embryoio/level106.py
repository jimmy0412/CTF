## a.py
fr = open('/tmp/aa','r')
fw = open('/tmp/bb','w')

import subprocess
import os

r = subprocess.Popen('/challenge/embryoio_level106',stdin=fr,stdout=fw)

r.wait()

# b.py
import os
import subprocess
fw = open('/tmp/aa','w')
fr = os.open('/tmp/bb',os.O_RDONLY)
r = subprocess.Popen('/usr/bin/cat',stdin=fr)
p = subprocess.Popen('/usr/bin/cat',stdout=fw)
p.wait() ## this is important



