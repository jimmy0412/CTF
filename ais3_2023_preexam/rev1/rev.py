enc =b"\x8A\x50\x92\xC8\x06\x3D\x5B\x95\xB6\x52\x1B\x35\x82\x5A\xEA\xF8\x94\x28\x72\xDD\xD4\x5D\xE3\x29\xBA\x58\x52\xA8\x64\x35\x81\xAC\x0A\x64\x00"
s = b"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&\()*+,-./:;<=>?@[]^_{|}~"

flag=b'AIS3{'
#for i in range(5):
count = 0
flag = ''
for i in range(6):
    tmp = enc[i]
    a = i ^ 9
    a = a & 3
    b = 8 - a
    for guess in s :
        if (((i ^ guess) << a)& 0xff | ((i ^ guess) >> b )) & 0xff == tmp -8:
            flag += chr(guess)

print(flag)
# for i in s :
#     guess = ((count ^ i )<< ((count ^ 9) >>3) | (count ^ i ) >> (8 - ((count ^ 9) >> 3))) + 8
#     print(hex(guess))
# for i in range(len(flag),len(a),1):
#     tmp = a[i]
#     tmp = tmp - 8
#     t = (i ^ 9) & 3 
#     tmp = tmp ^ i 
#     tmp = tmp >> t

#     print(chr(tmp))
