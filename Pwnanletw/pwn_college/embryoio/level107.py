#echo 'uhbwdqmo' >&205 | python a.py <&205

import subprocess
r = subprocess.Popen('/challenge/embryoio_level107',close_fds=False,stdin=205) ##close_fds=False is important
r.wait()


