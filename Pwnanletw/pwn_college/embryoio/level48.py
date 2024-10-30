from subprocess import Popen, PIPE
cmd1 = ['/challenge/embryoio_level48']
cmd2 = ['cat']

p1 = Popen(cmd1, stdout=PIPE, stderr=PIPE); p2 = Popen(cmd2, stdin=p1.stdout, stdout=PIPE) ; print("Output from last process: " + (p2.communicate()[0]).decode())