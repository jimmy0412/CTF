a = b'\x20\x24\x2b\x35\x3d\x40\x4e\x51\x53\x5c\x5e\x84\x85\x8c\x92\xa9\xab\xae\xb2\xb3\xbd\xc5\xd1\xd9\xdc\xea'
p = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
### reverse -> xor -> change -> xor -> bubble sort
### 9c 55 85 af c8
### 7->23 23->7
### a4 89 63 06 87

a0 = ''
a1 = ''
a2 = ''
a3 = ''
a4 = ''

a7 = ''
a23 = ''

flag =''
for i in range(0x1a):
    if chr(a[i] ^ 0x9c ^ 0xa4) in p:
        if(len(a0) < 6):
            a0 += chr(a[i] ^ 0x9c ^ 0xa4)
            continue
        
    if chr(a[i] ^ 0xc8 ^ 0x87) in p:
        if(len(a4) < 5):
            a4 += chr(a[i] ^ 0xc8 ^ 0x87)
            continue

    if chr(a[i] ^ 0x63 ^ 0xaf) in p:
        if(len(a7) < 1):
            a7 += chr(a[i] ^ 0x63 ^ 0xaf)
            continue

    if chr(a[i] ^ 0x85 ^ 0x63) in p:
        if(len(a2) < 4):
            a2 += chr(a[i] ^ 0x85 ^ 0x63)
            continue

    if chr(a[i] ^ 0x06 ^ 0x85) in p:
        if(len(a23) < 1):
            a23 += chr(a[i] ^ 0x06 ^ 0x85)
            continue
    if chr(a[i] ^ 0xaf ^ 0x06) in p:
        if(len(a3) < 4):
            a3 += chr(a[i] ^ 0xaf ^ 0x06)
            continue

    if chr(a[i] ^ 0x55 ^ 0x89) in p:
        if(len(a1) < 5):
            a1 += chr(a[i] ^ 0x55 ^ 0x89)
            continue 
print(f'a0 : {len(a0)}')
print(f'a1 : {len(a1)}')    
print(f'a2 : {len(a2)}')
print(f'a3 : {len(a3)}')
print(f'a4 : {len(a4)}')
print(f'a7 : {len(a7)}')
print(f'a23 : {len(a23)}')
   
for i in range(len(a)):
    if i%5 == 0 :
        flag += a0[i//5] 
    elif i%5 == 1:
        flag += a1[i//5]
    elif i%5 == 2:
        if i//5 == 1:
            flag += a7[0]
        elif i//5 == 0 :
            flag += a2[0]
        else:
            flag += a2[i//5-1] 
    elif i%5 == 3:
        if i//5 == 4:
            flag += a23[0]
        else:
            flag += a3[i//5]  
    else:
        flag += a4[i//5] 


print(flag[::-1])





