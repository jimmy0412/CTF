from pwn import *
import subprocess

arg = ['./share/chal']
#arg = ['nc','edu-ctf.zoolab.org','10002']
proc = subprocess.Popen(arg,stdin=subprocess.PIPE, stdout=subprocess.PIPE)
proc.communicate(input=b'\xc4')

print(proc.returncode)