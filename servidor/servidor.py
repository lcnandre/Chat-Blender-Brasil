﻿#porta e IP do servidor
PORTA = 2021
HOST = '127.0.0.1'

#variavel de controle do estado do servidor
global iniciado, clientes, s
iniciado = False
clientes = []
s = None

#importações
import socket
import threading

class Servidor():
	def __init__(self):
		pass
	#__init__

	def inicia(self):
		global iniciado, s
		#criacao do socket
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#colocacao do socket no IP e portas informadas
		s.bind((HOST, PORTA))
		#abertura do socket a novas conexoes
		s.listen(2)
		#inicio da thread que trata novas conexoes
		ThreadNovasConexoes().start()
		iniciado = True
	#inicia

	def para(self):
		global iniciado, s
		for cliente in clientes:
			cliente.close()
		s.close()
		s = None
		iniciado = False
	#para
#Servidor

#criacao da thread responsavel por tratar novas conexoes ao servidor
class ThreadNovasConexoes(threading.Thread):	
    def run (self):
		global iniciado, s
		while iniciado:
			con, end = s.accept() #aceitacao de nova conexao
			clientes.append(con) #colocacao do socket recem conectado na lista de clientes
			ThreadMensagensRecebidas(con).start() #inicio da thread que trata mensagens recebidas pelo cliente em questao
#ThreadNovasConexoes

#criacao da thread que trata mensagens recebidas por cada cliente
class ThreadMensagensRecebidas(threading.Thread):
    con = None #socket do cliente

    #inicializacao da thread e atribuicao do socket do cliente
    def __init__(self, con):
        self.con = con
        threading.Thread.__init__ (self)

    def run(self):
		global iniciado
		while iniciado: #loop infinito
			try: #tentativa de recepcao de dados do cliente
				dados = self.con.recv(1024)
				if len(dados) != 0: #se a mensagem nao esta em branco
					broadCast(dados) #envio da mensagem a todos os clientes
			except: #caso a tentativa falhe
				self.con.close() #fechamento do socket do cliente
				break #fim do loop infinito
#ThreadMensagensRecebidas

def broadCast(dados):
	for cliente in clientes: #para cada socket de cliente na lista
		cliente.send(dados) #envio da mensagem recebida
#broadCast