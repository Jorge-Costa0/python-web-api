from jinja2 import Environment, FileSystemLoader

# Configuração FIXA (só muda o caminho da pasta!)
env = Environment(loader=FileSystemLoader("."))

template = env.get_template('email.text')

data = {
    'name': 'Gox',
    'products': [
        {'name':'iphone', 'price':1800.00},
        {'name':'Zephyrus g14', 'price': 25000.00}
    ],
    'special_customer': True
}

try:
    print(template.render(**data))
except Exception as e:
    print(f"Erro ao renderizar template: {e}")