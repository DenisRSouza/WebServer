#implementação de um servidor base para interpratação de métodos HTTP

import socket
import os
import mimetypes

#definindo o endereço IP do host
SERVER_HOST = ""
#definindo o número da porta em que o servidor irá escutar pelas requisições HTTP
SERVER_PORT = 8080

#vamos criar o socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#vamos setar a opção de reutilizar sockets já abertos
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#atrela o socket ao endereço da máquina e ao número de porta definido
server_socket.bind((SERVER_HOST, SERVER_PORT))

#coloca o socket para escutar por conexões
server_socket.listen(1)

#mensagem inicial do servidor
print("Servidor em execução...")
print("Escutando por conexões na porta %s" % SERVER_PORT)

#cria o while que irá receber as conexões
while True:
    #espera por conexões
    #client_connection: o socket que será criado para trocar dados com o cliente de forma dedicada
    #client_address: tupla (IP do cliente, Porta do cliente)
    client_connection, client_address = server_socket.accept()

    #pega a solicitação do cliente
    request = client_connection.recv(4096)
    #verifica se a request possui algum conteúdo (pois alguns navegadores ficam periodicamente enviando alguma string vazia)
    if request:
        #imprime a solicitação do cliente
        #analisa a solicitação HTTP e separa o cabeçalho do corpo da requisição
        parsed_request = request.split(b'\r\n\r\n', 1)

        headers_text = parsed_request[0].decode('utf-8')
        body_text = parsed_request[1] if len(parsed_request) > 1 else b''

        


        parsed_headers_text = headers_text.split()
        metodo = parsed_headers_text[0]
        filename = parsed_headers_text[1]
        response = ''
        data = ''

        if metodo == "GET":
            try:
                print("METODO GET")
                
                with open ('htdocs' + filename, 'rb') as f:
                    data = f.read()

                response_header = []
                response_header.append(b"HTTP/1.1 200 OK")


                content_type, _ = mimetypes.guess_type(filename)
                if content_type:
                    response_header.append(f"Content-Type: {content_type}".encode('utf-8'))

                response_header.append(f"Content-Length: {len(data)}".encode('utf-8)'))

                client_connection.sendall(b'\r\n'.join(response_header) + b'\r\n\r\n' + data) #Vai enviar a resposta em bytes junto com o conteúdo do arquivo
                print(f"[GET] Arquivo '{filename}' enviado com sucesso")

            except Exception as e:
                response = b"HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/html\r\n\r\n <h2> ERROR 404 <br> FILE NOT FOUND <h2>"
                client_connection.sendall(response)
                print(f"[GET] ERRO ao enviar o arquivo: {e}")

        elif metodo == "POST":
            try:
                print("METODO POST")

                file_size = 0
                header_line = headers_text.split('\r\n')
                for line in header_line:
                    if line.lower().startswith('content-length:'): #eu tinha escrito content-lenght
                        # vai pegar o número que vem depois dos dois pontos e converte pra inteiro
                        file_size = int(line.split(':')[1].strip())

                body = body_text

                while len(body) < file_size:
                    pedaco = client_connection.recv(4096)
                    if not pedaco:
                        break
                    body += pedaco # Vai juntando os pedaços em bytes


                #fazendo o while pra verificar se já existe noticia{i}
                i = 1
                while True:
                    arquivo_html = f"noticia{i}.html"
                    caminho_html = os.path.join('htdocs', arquivo_html)
                    
                    if not os.path.exists(caminho_html): # se esse caminho não existir vai parar e criar o arquivo com esse nome
                        break
                    i += 1

                nome_imagem = f"imagem_noticia{i}.jpg"
                with open(os.path.join('htdocs', nome_imagem), 'wb') as f_img:
                    f_img.write(body) 
                
                with open(caminho_html, 'w', encoding='utf-8') as f_html:
                    f_html.write(f"<!DOCTYPE html><html><body><img src='{nome_imagem}'></body></html>")

                
                response = b"HTTP/1.1 201 Created\r\nContent-Type: text/html\r\n\r\n"
                response += f"<h2>A noticia {i} foi criada!</h2><a href='/{arquivo_html}'>Ver Noticia</a>".encode('utf-8')
                client_connection.sendall(response)
                
                print(f"[POST] '{arquivo_html}' e '{nome_imagem}' criados")

            except Exception as e:
                print(f"[POST] ERRO ao salvar o arquivo: {e}")
                response = b"HTTP/1.1 500 Internal Server Error\r\n\r\n<h2>Erro no servidor</h2>"
                client_connection.sendall(response)
                print(f"[POST] ERRO ao salvar o arquivo: {e}")

        else:
            response = b"HTTP/1.1 405 Method Not Allowed\r\n\r\n<h2>Metodo HTTP nao suportado</h2>"
            client_connection.sendall(response)
            print(f"[ERROR] Metodo HTTP '{metodo}' não suportado")

        
    #fecha a conexão com o cliente
    client_connection.close()

#OBS: tentar tirar o b do response pra parar o erro da linha 131


