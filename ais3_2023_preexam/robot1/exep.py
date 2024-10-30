from pwn import *
import os
import time
r = remote('chals1.ais3.org',12348)
#r = remote('localhost',1234)
r.recvuntil(b'Let\'s go!\n')
for i in range(29):
    cmd = r.recvline().strip().decode()
    print(cmd)
    ans = os.popen(f'python3 -c "print({cmd})"').readline()
    r.send(ans)
    time.sleep(0.1)
r.recvline()
for i in range(1):
    cmd = r.recvline().strip().decode()
    print(cmd)
    ans = os.popen(f'python3 -c "print({cmd})"').readline()
    r.send(ans)
    time.sleep(0.1)
r.interactive()