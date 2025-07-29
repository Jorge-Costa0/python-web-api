#carregar dados
dados = [
    {'nome':'Jorge', 'cidade':'Luanda','idade':'17'},
    {'nome':'Pedro', 'cidade':'Viana', 'idade':'21'}
]


#processar
template = '''\
<!doctype html>
<html>
<head></head>
<body>
    <ul>
        <li> Nome: {nome}</li>
        <li> cidade: {cidade}</li>
        <li> cidade: {idade}</li>
    </ul>
</body>
</hml>
'''
#renderizar
for item in dados:
    print(template.format(**item))