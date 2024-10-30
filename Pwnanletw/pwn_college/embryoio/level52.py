from subprocess import Popen, PIPE
cmd2 = ['/challenge/embryoio_level52']
cmd1 = ['cat']

p1 = Popen(cmd1, stdout=PIPE, stderr=PIPE); p2 = Popen(cmd2, stdin=p1.stdout, stdout=PIPE) ; print("Output from last process: " + (p2.communicate()[0]).decode())

#https://stackoverflow.com/questions/295459/how-do-i-use-subprocess-popen-to-connect-multiple-processes-by-pipes/16709666#16709666