# about get cmd output
# https://stackoverflow.com/questions/3503879/assign-output-of-os-system-to-a-variable-and-prevent-it-from-being-displayed-on
# a.sh  
# #!/bin/bash
# '/challenge/embryoio_level125'

from pwn import *
import os
r = process(['bash','/tmp/a.sh'])
r.recvuntil(b"This program will send you ")
count = int(r.recvuntil(b" ").strip())

for i in range(count):
    r.recvuntil(b'for: ')
    cal = r.recvline().strip().decode()
    cmd = f'python -c "print({cal})"'
    ans = os.popen(cmd).read().strip().encode()
    r.sendline(ans)


r.interactive()
