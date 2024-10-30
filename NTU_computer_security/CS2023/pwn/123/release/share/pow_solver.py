#!/usr/bin/env python3
import hashlib
import sys
from pwn import *
r = remote('10.113.184.121',10044)
r.recvuntil(b'sha256(')
a = r.recvuntil(b' +',drop=True).decode()
r.recvline()
prefix = a
difficulty = 22
zeros = '0' * difficulty

def is_valid(digest):
    if sys.version_info.major == 2:
        digest = [ord(i) for i in digest]
    bits = ''.join(bin(i)[2:].zfill(8) for i in digest)
    return bits[:difficulty] == zeros


i = 0
while True:
    i += 1
    s = prefix + str(i)
    if is_valid(hashlib.sha256(s.encode()).digest()):
        print(i)
        r.sendline(str(i).encode())
        r.wait(2)
        r.interactive()
        exit(0)

