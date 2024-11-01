from Crypto.Cipher import DES
from binascii import unhexlify
import itertools
res = '6020e9735ca3bf2f63aebcf3622c994880ffed2b509c91414c75d4c500ee80f4'
hint_pt = '414953337b3f3f3f3f3f3f3f3f3f3f7d'
hint = '118cd68957ac93b269335416afda70e6d79ad65a09b0c0c6c50917e0cee18c93'
iv = '4149533320e4b889'
iv1 = unhexlify(iv)
keyspace = b'\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff'
#possible = itertools.product(keyspace,repeat=8)
hint_pt = unhexlify(hint_pt)
hint = unhexlify(hint)
# for k1 in possible : 
count = 0
enc_list = {}

enc_l = []
# for i in itertools.product(keyspace,repeat=6):
#     key = bytes(i)
#     key = b'\xfa\xfa' + key
#     cipher = DES.new(key, DES.MODE_CBC,iv=iv1)
#     enc = cipher.encrypt(hint_pt)
#     enc_list[enc] = key

num = 0xffff
for i in itertools.product(keyspace,repeat=6):
    key = bytes(i)
    key = int.to_bytes(num,2,'big') + key
    enc_l.append(key)
print(f'good')
for i in enc_l:
    cipher = DES.new(i, DES.MODE_CBC,iv=iv1)
    enc = cipher.encrypt(hint_pt)
    enc_list[enc] = key

print(f'good')

for i in itertools.product(keyspace,repeat=7):
    key = bytes(i)
    for j in range(0xf0,0x100):    
        y = int.to_bytes(j,1,'little') + key
        #print(y)
        cipher = DES.new(y, DES.MODE_CBC,iv=iv1)
        dec = cipher.decrypt(hint)
        if dec in enc_list :
            k1 = enc_list[dec]
            print(f'k1 : {k1} k2 : {key}')
            break