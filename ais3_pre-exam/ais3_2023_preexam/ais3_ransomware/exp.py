import base64

f = open('./target_ais3/123.txt.ais3','rb+')
enc = f.read()
enc = base64.b64decode(enc)
print(enc)