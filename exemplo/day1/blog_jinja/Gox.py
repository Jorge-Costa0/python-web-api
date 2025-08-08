'''
1- orientaçao a objetos abstração
2- mapa de roteamento de URLS
3- configuração de templates
4- objeto callable (WSGI)
5- metodo 'run' execute a aplicação
'''
import os
import re
import json
from urllib.parse import parse_qs
from jinja2 import Environment, FileSystemLoader

class gox:
    def __init__(self):
        self.url_map = []
        self.templates_env = Environment(loader=FileSystemLoader('templates'))
        
    def route(self, rule, method="GET", template=None):
        def decorator(view):
            self.url_map.append((rule, method, view, template))
            return view
        return decorator
    
    def render_template(self, template_name, **context):
        template = self.templates_env.get_template(template_name)
        return template.render(**context).encode('utf-8')
    
    def serve_static(self, environ, start_response):
        """Middleware para servir arquivos estáticos"""
        path = environ['PATH_INFO'][len('/static/'):]  # Remove '/static/' do caminho
        static_dir = os.path.join(os.path.dirname(__file__), 'static')
        file_path = os.path.join(static_dir, path)
        
        # Prevenção contra directory traversal
        if not os.path.abspath(file_path).startswith(os.path.abspath(static_dir)):
            start_response('403 Forbidden', [('Content-type', 'text/html')])
            return [b'Access denied']
        
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                # Mapeamento de tipos MIME
                mime_types = {
                    '.css': 'text/css',
                    '.js': 'application/javascript',
                    '.png': 'image/png',
                    '.jpg': 'image/jpeg',
                    '.html': 'text/html'
                }
                ext = os.path.splitext(file_path)[1]
                content_type = mime_types.get(ext, 'text/plain')
                
                headers = [
                    ('Content-type', content_type),
                    ('Content-Length', str(len(content)))
                ]
                start_response('200 OK', headers)
                return [content]
            except Exception as e:
                start_response('500 Internal Server Error', [('Content-type', 'text/html')])
                return [b'Error reading static file']
        
        start_response('404 Not Found', [('Content-type', 'text/html')])
        return [b'Static file not found']

    def __call__(self, environ, start_response):
        try:
            path = environ['PATH_INFO']
            request_method = environ['REQUEST_METHOD']
            
            # Servir arquivos estáticos
            if path.startswith('/static/'):
                return self.serve_static(environ, start_response)
            
            # Resolver URLs
            for rule, method, view, template in self.url_map:
                if (match := re.match(rule, path)) and method == request_method:
                    view_args = match.groupdict()
                    
                    # Tratamento de formulários POST
                    if request_method == "POST":
                        try:
                            content_length = int(environ.get('CONTENT_LENGTH', 0))
                            post_data = environ['wsgi.input'].read(content_length).decode('utf-8')
                            view_args["form"] = {k: v[0] for k, v in parse_qs(post_data).items()}
                        except Exception as e:
                            view_args["form"] = {}
                    
                    # Executar a view
                    view_result = view(**view_args)
                    
                    # Processar o resultado
                    if isinstance(view_result, tuple):
                        body, status, *content_type = view_result
                        content_type = content_type[0] if content_type else 'text/html'
                    else:
                        body = view_result
                        status = "200 OK"
                        content_type = 'text/html'
                    
                    # Renderização
                    if template:
                        body = self.render_template(template, **body if isinstance(body, dict) else {})
                    elif content_type == "application/json":
                        body = json.dumps(body).encode('utf-8')
                    else:
                        body = str(body).encode('utf-8')
                    
                    headers = [('Content-type', content_type)]
                    start_response(status, headers)
                    return [body]
            
            # Rota não encontrada
            start_response('404 Not Found', [('Content-type', 'text/html')])
            return [b'<h1>404 Not Found</h1>']
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            start_response('500 Internal Server Error', [('Content-type', 'text/html')])
            return [b'<h1>500 Server Error</h1><p>Please try again later.</p>']
    
    def run(self, host='0.0.0.0', port=8000):
        from wsgiref.simple_server import make_server
        print(f"Servidor rodando em http://{host}:{port}")
        server = make_server(host, port, self)
        server.serve_forever()
