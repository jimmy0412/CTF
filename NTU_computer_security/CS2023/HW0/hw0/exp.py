from flask import Flask, Response, request, redirect
import re 
import random, string
app = Flask(__name__)

#url = "https://0270-140-112-42-143.ngrok-free.app/"

alias_dict = {}

@app.route("/",methods=['GET',"POST"])
def hello():

    text = request.data.decode()
    text = text.replace('[/gusp]','').replace('[gusp]','').split('|')
    url_len = text[1]
    url = text[2]

    ## len error
    # if url_len != len(url):
    #     error_message = "QQ len error"
    #     res = f'[gusp]ERROR|{len(error_message)}|{error_message}[/gusp]'
    #     r = Response(response=res, status=200, mimetype="application/xml")
    #     r.headers["Content-Type"] = "application/gusp"
    #     return r
    
    # alias
    if len(text) == 4 and text[3] != 'null':
        alias = text[3]
        print(alias)
    else :
        alias = ''.join(random.choice(string.ascii_letters) for _ in range(5))

    # duplicate alias 
    if alias in alias_dict or (len(text) == 4 and text[3] == 'null'):
        error_message = "QQ duplicated"
        res = f'[gusp]ERROR|{len(error_message)}|{error_message}[/gusp]'
        r = Response(response=res, status=200, mimetype="application/xml")
        r.headers["Content-Type"] = "application/gusp"
        return r
    else :
        alias_dict.update({alias:url})
        res = f'[gusp]SUCCESS|{len(alias)}|{alias}[/gusp]'
        r = Response(response=res, status=200, mimetype="application/xml")
        r.headers["Content-Type"] = "application/gusp"
        return r

@app.route("/<alias>",methods=['GET',"POST"])
def aaaaa(alias):
    if alias not in alias_dict:
        r = Response(response="page not found", status=404, mimetype="application/xml")
        r.headers["Content-Type"] = "application/gusp"
        return r

    return redirect(alias_dict[alias],code=302)

@app.route("/exp",methods=['GET',"POST"])
def exp():
    return redirect('/exp2',code=302)

@app.route("/exp2",methods=['GET',"POST"])
def exp2():
    return '123'

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000,debug=False)