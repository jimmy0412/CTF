from subprocess import Popen, PIPE
cmd2 = ['/challenge/embryoio_level53']
cmd1 = ['rev','/tmp/12']

p1 = Popen(cmd1, stdout=PIPE, stderr=PIPE); p2 = Popen(cmd2, stdin=p1.stdout, stdout=PIPE) ; print("Output from last process: " + (p2.communicate()[0]).decode())


##python -c 'print("cmdpmbze" + "\n"*888888)' > /tmp/12　create big file to delay rev process