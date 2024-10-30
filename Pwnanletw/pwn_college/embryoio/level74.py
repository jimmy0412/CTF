from pwn import *

cmd = ['/challenge/embryoio_level74']
for i in range(312) :
    cmd.append('azmroskkzk')
r = process(cmd)

r.interactive()


