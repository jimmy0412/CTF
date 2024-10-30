from binascii import unhexlify

a = '0525723D4F2F5701573B54213B51024D15421E51187A271A760943114311472D24507C263C772722262C7F7F0E777C37616D316F62693646353C203F396C363C50'
#f = b'FLAG{aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa}'
c = b'Ch1y0d4m0m0'
b = unhexlify(a)
flag = ''
d = b''

for i in range(65):
    x = i ^ c[i % len(c)]
    y = x ^ b[i]
    flag += chr(y)


print(flag)




