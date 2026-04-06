# WebServer

Servidor HTTP simples feito em Python usando sockets TCP.

Este projeto implementa, de forma didatica, um servidor que:

- Recebe requisicoes HTTP na porta `8080`
- Responde arquivos estaticos com `GET` (ex.: `index.html`, `index.css`, imagens)
- Processa envio de formulario com `POST` (`multipart/form-data`)
- Cria novas noticias dinamicamente em `htdocs/`, incluindo:
  - Um arquivo HTML da noticia (`noticia1.html`, `noticia2.html`, etc.)
  - Uma imagem da noticia (`imagem_noticia1.jpg`, etc.)
  - Atualizacao do arquivo `news.json` com os metadados da noticia (usado para atualizar dinamicamente o home feed de noticias)

## Estrutura

```
.
├── servidorHTTP.py
└── htdocs/
		├── index.html
		├── index.css
		├── index.js
		└── noticia.css
```

## Requisitos

- Python 3
- Navegador web (Chrome, Firefox, etc.)

## Como executar

No diretorio do projeto, rode:

```bash
python3 servidorHTTP.py
```

Voce deve ver algo como:

```text
Servidor em execucao...
Escutando por conexoes na porta 8080
```

## Como testar o servidor

1. Com o servidor rodando, abra no navegador:
   - `http://localhost:8080/index.html`
2. Crie uma noticia no formulario presente na pagina

3. Apos criado, a pagina deve atualizar sua home feed automaticamente para aparecer as novas noticias publicadas

4. Clique no card da nova noticia publicada para entrar na tela da noticia

5. Utilize o botao 'voltar' para retornar ao home de noticias
