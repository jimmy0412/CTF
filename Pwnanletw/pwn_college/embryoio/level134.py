import subprocess
import os
p = subprocess.Popen(['cat'],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
p2 = subprocess.Popen('/challenge/embryoio_level134',stdin=p.stdout,stdout=subprocess.PIPE)
p3 = subprocess.Popen('cat',stdin=p2.stdout,stdout=subprocess.PIPE)

for i in range(51) :
    while True :
        a = p3.stdout.readline().decode()
        #print(a)
        if 'solution' in a :
            cal = a.split('for: ')[1].strip()
            ans = os.popen(f'python -c "print({cal})"').read().strip() + '\n'
            #print(ans)
            p.stdin.write(ans.encode())
            p.stdin.flush()
            break
        if 'pwn' in a :
            print(a)
            break




### test
p1 = process('cat',stdout=PIPE)
p2 = process('/challenge/embryoio_level134',stdout=PIPE,stdin=p1.stdout)
p3 = process('cat',stdin=p2.stdout)

p1.wait()
p2.wait()
p3.wait()
p3.interactive()


### c.py
import subprocess
from pwn import *
import sys
r = process(['python','a.py'],stdout=sys.stdout,stdin=sys.stdin,shell=True)
r.interactive()
#r = subprocess.run(['python','a.py'])
