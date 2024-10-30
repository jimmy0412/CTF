#a.py
fr = open('/tmp/aa','r')
from pwn import *
r = process('/challenge/embryoio_level103',stdin=fr)


# b.py
fw = open('/tmp/aa','w')
fw.write("ijflgrfj")
fw.flush()

##cmd 
#python b.py & python a.py
##ref : https://stackoverflow.com/questions/7048095/how-do-i-properly-write-to-fifos-in-python