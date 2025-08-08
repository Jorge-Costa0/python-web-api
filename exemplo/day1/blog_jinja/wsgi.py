from database import conn
import json
from urllib.parse import parse_qs
from jinja2 import Environment, FileSystemLoader


env = Environment(loader=FileSystemLoader('templates'))

def get_posts_from_database(post_id=None):
    cursor = conn.cursor() 
    fields = ('id', 'title', 'content', 'author')

    if post_id:
        results = cursor.execute('SELECT * FROM post WHERE id = ?;', post_id)
    else:
        results = cursor.execute('SELECT * FROM post')
    return [dict(zip(fields, post)) for post in results]

def render_template(template_name, **context):
    template = env.get_template(template_name)
    return template.render(**context).encode('utf-8')


def add_new_post(post):
    cursor = conn.cursor()
    cursor.execute(
        '''\
        INSERT INTO post (title, content, author)
        VALUES (:title, :content, :author)
        ''',
        post
    )
    conn.commit()

def application(environ, start_response): 
    body = b'Content Not Found'
    status = '404 Not Found'
    content_type = 'text/html'
    
    path = environ['PATH_INFO']
    method = environ['REQUEST_METHOD']

    if path == '/' and method == 'GET':
        posts = get_posts_from_database()
        body = render_template(
            'list.template.html',post_list=posts
        )
        status = '200 OK'
    elif path == '/api' and method == 'GET':
        posts = get_posts_from_database()
        body = json.dumps(posts).encode('utf-8') # processo de serialização
        content_type = 'application/json' # MINE TYPES
        status = '200 OK'
        
    elif path.split('/')[-1].isdigit() and method == 'GET':
        post_id = path.split('/')[-1]
        body = render_template(
            'post.template.html',
            post=get_posts_from_database(post_id=post_id)[0]
        )
        status = '200 OK'
    elif path == '/new' and method == 'GET':
        body = render_template('form.template.html')
        status = '200 OK'
    elif path == '/new' and method == 'POST':
        try:
            # Método moderno para processar POST data
            content_length = int(environ.get('CONTENT_LENGTH', 0))
            post_data = parse_qs(environ['wsgi.input'].read(content_length).decode('utf-8'))
            post = {k: v[0] for k, v in post_data.items()}
            add_new_post(post)
            body = b'New post created with success!'
            status = '201 Created'
        except Exception as e:
            status = '400 Bad Request'
            body = f'Error processing form: {str(e)}'.encode('utf-8')
    
    # criar o response 
    headers = [('Content-type', content_type)]
    start_response(status, headers)
    return [body]