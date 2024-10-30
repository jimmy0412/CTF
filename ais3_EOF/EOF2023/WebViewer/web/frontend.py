from subprocess import run, PIPE
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib.parse import urlparse, parse_qs

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.set_headers()
        if self.path == '/backdoor':
          return self.do_not_call_this_function_its_only_for_debugging_purposes()
        return self.wfile.write(self.make_template("""
        <form method=POST enctype="text/plain">
        <textarea name=urls id=urls placeholder="http://example.com/, http://example.com/notexist"></textarea>
        <input type=submit value=View>
        </form>
        """))

    def do_POST(self):
        self.set_headers()
        data_string = self.rfile.read(int(self.headers['Content-Length'])).decode()[5:] # strip('urls=')
        ret = run(['node', 'backend.js', data_string], stdout=PIPE, text=True, timeout=5).stdout
        return self.wfile.write(self.make_template(ret))

    def set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def make_template(self, html):
        html = f'''
        <title>WebViewer</title>
        <link rel="stylesheet" href="https://cdn.simplecss.org/simple.css">
        <body><main><h1>WebViewer</h1>{html}</main></body>
        '''
        return html.encode('utf8')

    def do_not_call_this_function_its_only_for_debugging_purposes(self):
        if self.headers['host'] != 'localhost':
          return self.wfile.write(self.make_template('forbidden'))
        cmd = parse_qs(urlparse(self.path).query).get('cmd') or ['id']
        ret = run(cmd, stdout=PIPE, text=True, timeout=5).stdout
        return self.wfile.write(self.make_template(ret))

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == "__main__":
    server = ThreadedHTTPServer(('0.0.0.0', 5000), Handler)
    server.serve_forever()

