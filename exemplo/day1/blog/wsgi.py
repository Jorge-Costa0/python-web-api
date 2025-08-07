import cgi
from pathlib import Path
from database import conn

def get_posts_from_database(post_id=None):
    cursor = conn.cursor() 
    fields = ('id', 'title', 'content', 'author')

    if post_id:
        results = cursor.execute('SELECT * FROM post WHERE id = ?;', post_id)
    else:
        results = cursor.execute('SELECT * FROM post')
    return [dict(zip(fields, post)) for post in results]

def render_template(template_name, **context):
    template = Path(template_name).read_text()
    return template.format(**context).encode('utf-8')

def get_post_list(posts):
    post_list = [
    f"""<li> <a href='/{post['id']}'> {post['title']} </a> </li>"""
    for post in posts
    ]
    return '\n'.join(post_list)

def add_new_post(post):
    cursor = conn.cursor()
    cursor.execute(
        '''\
            INSERT INTO post (title, content, author),
            VALUES (:title, :content, :author),
        ''',
        post
    )
    conn.commit()

def application(environ, start_response): 
    body = b'content Not Found'
    status = '404 Not Found'
    #processar o request
    path = environ['PATH_INFO']
    method = environ['REQUEST_METHOD']

    #roteamento de rotas/URLs
    if path == '/' and method == 'GET':
        pasts = get_posts_from_database()
        body = render_template(
            'list.template.html',
            posts_list= get_post_list(pasts)
        )
        status = '200 OK'
    elif path.split('/')[-1].isdigit() and method == 'GET':
        post_id = path.split('/')[-1]
        body = render_template(
            'post.template.html',
            post=get_posts_from_database(post_id=post_id)[0]
        )
        status = '200 OK'
    elif '/new' and method == 'GET':
        body = render_template('form.template.html')
        status = '200 OK'
    elif '/new' and method == 'GET':
        form = cgi.FieldStorege(
            fp=environ['wsgi.input']
            environ=environ,
            keep_blank_values=1
        )
        post = {item.name: item.value for item in form.list}
        add_new_post(post)
        body = b'New post created with sucess!'
        staus = '201 created'
     #criar o request
        headers = [('content-type', 'text/html')]
        start_response(status, headers)
    return [body]
