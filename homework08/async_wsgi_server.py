import async_http_server
import sys


class AsyncWSGIServer(async_http_server.AsyncServer):

    def set_app(self, application):
        self.application = application

    def get_app(self):
        return self.application


class AsyncWSGIRequestHandler(async_http_server.AsyncHTTPRequestHandler):

    def get_environ(self):
        env = {}
        env['wsgi.version']      = (1, 0)
        env['wsgi.url_scheme']   = 'http'
        env['wsgi.input']        = sys.stdin
        env['wsgi.errors']       = sys.stderr
        env['wsgi.multithread']  = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once']     = False
        env['REQUEST_METHOD']    = self.request_method    
        env['PATH_INFO']         = self.path              
        env['SERVER_NAME']       = self.server_name       
        env['SERVER_PORT']       = str(self.server_port)  
        return env


    def start_response(self, status, response_headers, exc_info=None):
        code, message = status.split(" ")
        self.init_response(code, message)
        for key, value in response_headers:
            self.headers[key] = value
        
    def handle_request(self):
        env = self.get_environ()
        app = server.get_app()
        result = app(env, self.start_response)
        self.finish_response(result)
        
    def finish_response(self, result):
        self.begin_response(self.response_code, self.response_message)
        for data in result:
            self.push(data)
        self.end_response()
        self.close()

def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b'Hello World']

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Provide a WSGI application object as module:callable')
    app_path = sys.argv[1]
    module, application = app_path.split(':')
    module = __import__(module)
    application = getattr(module, application)
    server = AsyncWSGIServer(handler_class=AsyncWSGIRequestHandler)
    server.set_app(application)
    server.serve_forever()
