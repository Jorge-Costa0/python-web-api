from pathlib import Path
from database import conn

# obter os dados
cursor = conn.cursor()
fields = ('id', 'title', 'content', 'author')
results = cursor.execute('SELECT * FROM post;')
posts = [dict(zip(fields, post)) for post in results]
print(posts)

# 2 criar a pasta de destino do site
site_dir = Path('site')
site_dir.mkdir(exist_ok=True)


# 3 ccriar uma função para gerar a url com slug
def get_post_url(post):
    slug = post['title'].lower().replace(' ', '-')
    return f'{slug}.html'

# renderizar a pagina index.html

index_template = 