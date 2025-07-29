# 1 conectar com o banco de dados
from sqlite3 import connect
conn = connect('blog.db')
cursor = conn.cursor()

# 2 definir e criar a table
conn.execute(
    '''\
    CREATE TABLE if not exists post (
        id integer PRIMARY KEY AUTOINCREMENT,
        title varchar UNIQUE NOT NULL,
        content varchar NOT NULL,
        author varchar NOT NULL
    );
    '''
)

posts = [
    {
        'title': 'O que é uma API',
        'content': '''\
        A API é como se fosse o garçom de um restaurante — ela leva seu pedido até a cozinha (servidor) e traz a resposta (os dados). 
        É  o meio de comunicação entre o cliente (navegador, app) e o servidor.''',
        'author': 'Dev Gox'
    },
    {
        'title': 'Como funciona o Frontend e o Backend',
        'content': '''\
        O frontend é tudo o que o usuário vê e interage, como botões, textos e imagens. 
        O backend é o cérebro por trás disso — processa dados, conecta com o banco e envia as respostas para o frontend.''',
        'author': 'Dev Gox'
    },
    {
        'title': 'O que é um Banco de Dados',
        'content': '''\
        Um banco de dados é como uma estante digital que guarda informações organizadas. 
        Pode conter usuários, produtos, senhas, textos e muito mais. O backend conversa com ele o tempo todo.''',
        'author': 'Dev Gox'
    },
    {
        'title': 'O que é HTTP e HTTPS',
        'content': '''\
        HTTP é o protocolo que os navegadores usam para se comunicar com servidores. 
        HTTPS é a versão segura — com criptografia — que protege os dados enquanto viajam pela internet.''',
        'author': 'Dev Gox'
    },
    {
        'title': 'O que é JSON',
        'content': '''\
        JSON (JavaScript Object Notation) é um formato leve para trocar dados entre sistemas. 
        É  como uma linguagem universal que servidores e aplicativos entendem, com estrutura de chave e valor.''',
        'author': 'Dev Gox'
    }
]

# 4 inserimos os posts caso o banco de dados esteja vazio
count = cursor.execute('SELECT * FROM post;').fetchall()
if not count:
    cursor.executemany(
        '''\
        INSERT INTO post (title, content, author)
        VALUES (:title, :content, :author);
        ''',
        posts,
    )
    conn.commit()

# 5 verificamos que foi realmente inserido
posts = cursor.execute('SELECT * FROM post;').fetchall()
assert len(posts) >= 2