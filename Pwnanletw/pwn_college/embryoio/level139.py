from pwn import *

r = process('cat | ~/a | cat',shell=True)
r.recvuntil(b"This program will send you ")
count = int(r.recvuntil(b" ").strip())

for i in range(count):
    r.recvuntil(b'for: ')
    cal = r.recvline().strip().decode()
    cmd = f'python -c "print({cal})"'
    ans = os.popen(cmd).read().strip().encode()
    r.sendline(ans)
r.interactive()

