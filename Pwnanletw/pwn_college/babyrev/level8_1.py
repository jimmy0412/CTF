## reverse 
### change 5 32 
### xor 4f 36 79 21 4b f7 81
### bubble sort
### change 5 16
### change 2 29
### reverse
p = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
a = b'\xf8\xf6\xed\xea\xe7\x9a\x92\x84\x84\x81\x5d\x5b\x52\x4f\x4c\x46\x44\x44\x43\x42\x42\x41\x3e\x3d\x3c\x3a\x39\x2f\x2b\x26\x24\x23\x21\x1d\x1c\x1c\x17\x10\x01'

a = a[::-1]

c0 = ''
c1 = ''
c2 = ''
c3 = ''
c4 = ''
c5 = ''
c6 = ''
for i in range(len(a)):
    if chr(a[i] ^ 0x79) in p:
        if(len(c2) < 6):
            c2 += chr(a[i] ^ 0x79)
            continue

    if chr(a[i] ^ 0x21) in p:
        if(len(c3) < 6):
            c3 += chr(a[i] ^ 0x21)
            continue

    if chr(a[i] ^ 0x81) in p:
        if(len(c6) < 5):
            c6 += chr(a[i] ^ 0x81)
            continue      

    if chr(a[i] ^ 0x4b) in p:
        if(len(c4) < 5):
            c4 += chr(a[i] ^ 0x4b)
            continue 

    if chr(a[i] ^ 0x36 ) in p:
        if(len(c1) < 6):
            c1 += chr(a[i] ^ 0x36)
            continue


    if chr(a[i] ^ 0x4f) in p:
        if(len(c0) < 6):
            c0 += chr(a[i] ^ 0x4f)
            continue
        








    if chr(a[i] ^ 0xf7) in p:
        if(len(c5) < 5):
            c5 += chr(a[i] ^ 0xf7)
            continue    



print(f'a0 : {len(c0)}')
print(f'a1 : {len(c1)}')    
print(f'a2 : {len(c2)}')
print(f'a3 : {len(c3)}')
print(f'a4 : {len(c4)}')    
print(f'a5 : {len(c5)}')
print(f'a6 : {len(c6)}')
c = ''
for i in range(len(a)):
    if i%7 == 0:
        c += c0[i//7]
    elif i%7 == 1:
        c += c1[i//7]
    elif i%7 == 2 :
        c += c2[i//7]
    elif i%7 == 3 :
        c += c3[i//7]
    elif i%7 == 4 :
        c += c4[i//7]
    elif i%7 == 5 :
        c += c5[i//7]        
    else:
        c += c6[i//7]

flag = ' '

for i in range(len(c)):
    if i == 5 :
        flag += c[32]
    elif i == 32 :
        flag += c[5]
    else :
        flag += c[i]

print(flag[::-1])





