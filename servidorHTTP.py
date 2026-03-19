#implementação de um servidor base para interpratação de métodos HTTP

import socket
import os

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
    request = client_connection.recv(4096) #tive que tirar o decode porque ele não lia imagens pq eh texto
    #verifica se a request possui algum conteúdo (pois alguns navegadores ficam periodicamente enviando alguma string vazia)
    if request:
        #imprime a solicitação do cliente
        
        #analisa a solicitação HTTP e separa o cabeçalho do corpo da requisição
        headers_bytes = request.split(b'\r\n\r\n', 1)
        #print(headers)#impressão dos cabeçalhos
        #pega o nome do arquivo sendo solicitado


        #como tirei o decode precisamos decodificar a parte do cabeçalho pra ler o texto

        header_text = headers_bytes[0].decode('utf-8', errors = 'ignore')
        headers = [header_text]
        
        #if len(headers_bytes) > 1:
         #   headers.append(headers_bytes[1].decode('utf-8', errors = 'ignore')) Já trocou

        linha_pedido = headers[0].split()
        metodo = linha_pedido[0]

        print(metodo)
        filename = linha_pedido[1]
        filename = os.path.basename(filename)
        print(filename)

        print(metodo)
        response = ''
        if metodo == "GET":
            try:
                print("METODO GET")
                fin = open('htdocs/'+filename, 'rb') #rb para ler em bytes
                content = fin.read()
                fin.close()

                response_header = b"HTTP/1.1 200 OK\r\n\r\n" 
                #tava dando erro pois o fin estava abrindo o arquivo como string e o response_header tinha um b para ler em bytes

                client_connection.sendall(response_header + content) #Vai enviar a resposta em bytes junto com o conteúdo do arquivo
                print(f"[GET] Arquivo '{filename}' enviado com sucesso")

            except FileNotFoundError:
                response = b"HTTP/1.1 404 NOT FOUND\r\n\r\n<h2> ERROR 404 <br> FILE NOT FOUND <h2>"
                client_connection.sendall(response) #tava dando errado pq tinha colocado client_connection.sendall(response_header + content)
                print(f"[GET] ERROR 404 Arquivo '{filename}' não foi encontrado")

        elif metodo == "POST":
            try:
                print("METODO POST")

                file_size = 0
                header_line = headers_text[0].split('\r\n')
                for line in header_line:
                    if line.lower().startswith('content-length:'): #eu tinha escrito content-lenght
                        # vai pegar o número que vem depois dos dois pontos e converte pra inteiro
                        file_size = int(line.split(':')[1].strip())

                body = headers[1].encode() if len(headers) > 1 else b'' # se não existir headers[1] então o body vai ser um corpo vazio de bytes

                while len(body) < file_size:
                    pedaco = client_connection.recv(4096)
                    if not pedaco:
                        break
                    body += pedaco # Vai juntando os pedaços em bytes

                with open('htdocs/' + filename, 'wb') as fout:
                    fout.write(body)
                
                #Enviar a resposta de sucesso (201 Created)
                response = b"HTTP/1.1 201 Created\r\n\r\n<h2>Arquivo salvo no servidor com sucesso!</h2>"
                client_connection.sendall(response)
                print(f"[POST] Arquivo '{filename}' salvo com sucesso!")

            except Exception as e:
                
                response = b"HTTP/1.1 500 Internal Server Error\r\n\r\n<h2>Erro no servidor</h2>"
                client_connection.sendall(response)
                print(f"[POST] ERRO ao salvar o arquivo: {e}")

        client_connection.sendall(response.encode())

        client_connection.close()

server_socket.close()

#OBS: tentar tirar o b do response pra parar o erro da linha 131


