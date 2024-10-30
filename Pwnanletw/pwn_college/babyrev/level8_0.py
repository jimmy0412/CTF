# len = 0x23

## change 18 27
## rev -> xor 4b c8 22 7d -> rev -> bubble -> rev
## change 3 7
p = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
a = '\xbc\xbb\xbb\xa5\xad\xac\xaa\xb9\xa3\x57\x57\x54\x53\x4b\x4a\x48\x48\x40\x3c\x32\x2d\x2a\x28\x27\x26\x23\x20\x1f\x19\x19\x13\x0e\x0a\x07\x05'
## change 3 7 
a = b'\xbc\xbb\xbb\xb9\xad\xac\xaa\xa5\xa3\x57\x57\x54\x53\x4b\x4a\x48\x48\x40\x3c\x32\x2d\x2a\x28\x27\x26\x23\x20\x1f\x19\x19\x13\x0e\x0a\x07\x05'

c0 = ''
c1 = ''
c2 = ''
c3 = ''
for i in range(0x23):
    if chr(a[i] ^ 0x4b) in p:
        if(len(c0) < 9):
            c0 += chr(a[i] ^ 0x4b)
            continue
        
    if chr(a[i] ^ 0xc8 ) in p:
        if(len(c1) < 9):
            c1 += chr(a[i] ^ 0xc8)
            continue

    if chr(a[i] ^ 0x22) in p:
        if(len(c2) < 9):
            c2 += chr(a[i] ^ 0x22)
            continue

    if chr(a[i] ^ 0x7d) in p:
        if(len(c3) < 8):
            c3 += chr(a[i] ^ 0x7d)
            continue


print(f'a0 : {len(c0)}')
print(f'a1 : {len(c1)}')    
print(f'a2 : {len(c2)}')
print(f'a3 : {len(c3)}')
c = ''
for i in range(0x23):
    if i%4 == 0:
        c += c0[i//4]
    elif i%4 == 1:
        c += c1[i//4]
    elif i%4 == 2 :
        c += c2[i//4]
    else:
        c += c3[i//4]
c =  c[::-1]
flag = ''
for i in range(len(c)):
    if i == 18 :
        flag += c[27]
    elif i == 27 :
        flag += c[18]
    else :
        flag += c[i]


print(flag)