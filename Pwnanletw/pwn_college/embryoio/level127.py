from pwn import *
import subprocess
r = process(['bash','/tmp/a.sh'])

r.recvuntil(b'(PID ')
pid = r.recvuntil(b')').decode().split(')')[0]
print(pid)

r.recvuntil(b"['")
sig = r.recvuntil(b"']").decode().split("']")[0]
sig = sig.split("', '")
cmd = ['kill','-s',' ',pid]
for i in sig:
    cmd[2] = i
    subprocess.run(cmd)
    r.recvuntil(b'Correct!\n')

r.interactive()
