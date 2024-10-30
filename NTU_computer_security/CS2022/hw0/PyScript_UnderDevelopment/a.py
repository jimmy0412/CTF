from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_geek():
    return '<h1>This challenge is still under development QQ</h2>'


if __name__ == '__main__':
    app.debug = True
    app.run("0.0.0.0")
