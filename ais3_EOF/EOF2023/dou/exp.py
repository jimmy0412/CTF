import hashlib
from binascii import unhexlify
m = hashlib.md5()
a = [49,8,83,209,4,77,130,36,139,44,248,52,172,0,207,23,17,27,97,254,30,116,143,28]
#f = open('qqq','wb+')
for i in range(1000,10000):
    flag = ''
    data = str(i).encode()
    m = hashlib.md5()
    m.update(data)
    h = m.hexdigest()
    unhex = unhexlify(h)

    for i in range(len(a)):
        #x = a[i] ^ unhex[i % len(unhex)]
        flag += chr(a[i] ^ unhex[i % len(unhex)])
    
    if 'FLAG' in flag :
        print(flag)
        break