from pwn import *


f = open('./mno2','rb+')



f.seek(0x890)
test = b''
while test != b'%s' :
    test = b''
    while True :       
        a = f.read(1)
        if a == b'\x00' :
            break
        test += a
    print(test)
    print(disasm(test, arch = 'i386'))
    