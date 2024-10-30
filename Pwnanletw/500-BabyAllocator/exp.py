from pwn import * 

r = process('./B', env = {"LD_PRELOAD" : "./libc_64.so.6"})

def alloc_stack(size,name): # 0x7f < size < 0xfff , name < 0x10 
    r.sendafter(b'Your choice:',b'1')
    r.sendafter(b'Size :',str(size))
    r.sendlineafter(b'allocator ? :',name)

def alloc_heap(size,name): # 0xff < size , name < 0x10 
    r.sendafter(b'Your choice:',b'2')
    r.sendafter(b'Size :',str(size))
    r.sendlineafter(b'allocator ? :',name)

def write_data(data):
    r.sendlineafter(b'Your choice:',b'3')
    r.send(data)

def create():
    r.sendlineafter(b'Your choice:',b'4')

def release():
    r.sendlineafter(b'Your choice:',b'5')
#alloc_stack(0x100,b'1234')
#alloc_heap(0x100,b'1234')
#write_data(b'jkljlk')
r.interactive()
