from flask import Flask, url_for, request
from flask_pymongo import PyMongo

app = Flask(__name__)

#configuração
app.config['APP_NAME'] = 'Kazu' # Configuração primeiro 
app.config['MONGO_URI']  = 'mongodb://localhost:27017/blog'  # Inicialização depois

mongo = PyMongo(app)

@app.errorhandler(404)
def not_found_page(error):
    return f'Desculpa ae mn, Não foi encontrado nada na {app.config['APP_NAME']}'
#app.register_error_handler(404, not_found_page)

#aplicação
@app.route('/')
def home():
    posts = mongo.db.posts.find()
    Content_url = url_for('read_content', title='novidade de 2025')
    return (
        f'<h1>{app.config['APP_NAME']}</h1>'
        f'<a href="{Content_url}"> Novidades de 2025'
        '<hr>'
        # request
        f'{list(posts)}'
    )
@app.route('/<title>')
def read_content(title):
    index_url = url_for('home')
    return f'<h1>{title}</h1> <a href="{index_url}"> Volar</a>'

#app.add_url_rule('/<title>', view_func=read_content)