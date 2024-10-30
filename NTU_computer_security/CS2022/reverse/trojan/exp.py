from binascii import unhexlify
key = b"0vCh8RrvqkrbxN9Q7Ydx\x00"


f = open('./data.txt','rb+')

enc = f.read()
enc = unhexlify(enc)

f1 = open('2.png','wb+')
key_len = len(key)
for i in range(len(enc)) :
    f1.write((enc[i] ^ key[i%key_len]).to_bytes(1,'little'))
    #f1.write(chr(enc[i] ^ key[i%key_len]).encode())
    