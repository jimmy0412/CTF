a = b'admin'
b = b'NYKD54'
c = 0x12348765 
e = 0
for i in range(len(a)):
    d = b[i%len(b)] ^ a[i]
    e = d ^ e
    e = e * c & 0xffffffff
    print(hex(e))
