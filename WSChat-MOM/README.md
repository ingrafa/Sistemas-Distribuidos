# WSChat-MOM
Chat usando WebService e Middleware Orientado à Mensagens


## Como executar:

### Instalando requisitos
Em uma máquina com Python 2, execute:
```
$ pip install -r requirements.txt
```
Além destes pacotes é necessário que sua máquina possua:
* omniORB (http://omniorb.sourceforge.net/)
* RabbitMQ (https://www.rabbitmq.com/)
* Tkinter (https://docs.python.org/2/library/tkinter.html)

### Execute o ORB:

```
$ omniNames -start -datadir .
```

### Execute o servidor:
```
$ python server.py
```


### Executando o arquivo principal:
Com  servidor executando normalmente, no diretório principal do projeto, execute o seguinte comando para iniciar o chat:
```
$ python start_client.py
```


## Observacoes
Requisitos do projeto: https://github.com/Ryllari/WSChat-MOM/blob/master/Projeto5.pdf

Autor: Ryllari R. M. Santana

#### Este projeto foi desenvolvido para o trabalho da disciplina de Programacao Paralela e Distribuída do curso de Engenharia de Computacao do IFCE Campus Fortaleza