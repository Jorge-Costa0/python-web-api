# callable - funçao(), obj(), (lambda)(...)

def application(environ, start_response):
    # faz oq quiser com o request
    print(environ)


    status = '200 OK'
    header = [('content-type', 'text/html')]
    body = b'<strong>hello world</strong>'
    start_response(status, header)
    return [body]


if __name__ == 'name':
    from wsgiref.simple_server import  make_server
    server = make_server('0.0.0.0', 8000,application)
    server.serve_forever()

#uwsgi