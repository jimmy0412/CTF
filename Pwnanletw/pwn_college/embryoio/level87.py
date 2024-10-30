from pwn import *

r = process('/challenge/embryoio_level87')

r.recvuntil(b"solution for: ")
cal = r.recvline().strip()
print(cal)

r.interactive()



