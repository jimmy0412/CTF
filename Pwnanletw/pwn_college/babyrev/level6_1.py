count = 0
a = b'\x41\x43\x44\x45\x4d\x4f\x59\x5a\x82\x85\x85\x88\x8d\x95\x97\x9d\x9f'
p = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
assert(len(a) == 0x11)
flag = ''
b = ''
c = ''
for i in range(17) :
    if chr(a[i] ^ 0x37) in p:
        b += chr(a[i] ^ 0x37)
    else:
        c += chr(a[i] ^ 0xef)


for i in range(17):
    if i % 2 == 0 :
        flag += c[i//2]
    else :
        flag += b[i//2]

print(flag)