import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 9000))
server.listen()

try:
    while True:
        client, addres = server.accept()
        #request
        data = client.recv(5000).decode()
        print(f'{data=}')

        #response
        client.sendall(
            'HTTP/1.0 200 OK\r\n\r\n<html>\r\n<head></head>\r\n<body>\r\n<h1>Hello, world!</h1>\r\n</body>\r\n</html\r\n\r\n'.encode()
        )
        client.shutdown(socket.SHUT_WR)


except Exception:
    server.close()