from re import L
import string
count = 0 
a= b'\xcc\xa0\x1c\xc5\xa4\x06\xde\xbc\x03\xc0\xb5\x18\xcb\xb9\x06'
payload = a[::-1]
print(payload)
flag = ''
for i in range(15):
    a = i * 0x55555556 >> 0x20
    b = i >> 0x1f
    a = a - b
    a = a * 3
    c = i 
    c = c - a

    if c == 0 :
        d = payload[i] ^ 0x69
    if c == 1 :
        d = payload[i] ^ 0xd7
    if c == 2 :
        d= payload[i] ^ 0xa7

    flag += chr(d)

b = 0x20-0x1b
c = 0x20-0x18
print(flag)
a = ''
for i in range(15) :
    if i == b :
        a += flag[c]
    elif i == c :
        a += flag[b]
    else : 
        a += flag[i] 

print(a)
