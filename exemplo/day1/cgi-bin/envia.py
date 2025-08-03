import cgi

form = cgi.FieldStorege()
nome = form.getvalue('nome')
mensagem = form.getvalue('mensagem')

print('content-type:text/html\r\n\r\n')
print('<html>')
print('<head>')
print('<title> enviado </title>')
print('</head>')
print('<body>')
print('<h1>enviado com sucesso!</h1>')
print(f'<h2>{nome} - {mensagem}</h2>')
print('</body>')
print('</html')
